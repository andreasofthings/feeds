#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:py:mod:`feeds.tasks`
=====================

Async tasks, run via celery, updated to work with celery3.

This module takes care of everything that is not client/customer facing.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

import logging
logger = logging.getLogger(__name__)

import datetime
import feedparser
import calendar
from collections import Counter

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from feeds import FeedErrorHTTP, FeedErrorParse, FeedSame
from .models import Feed, Post
from .models import FeedEntryStats


def entry_guid(entry, feed_has_no_guid=None):
    """
    Get an individual guid for an entry
    """
    guid = ""

    if entry.link or feed_has_no_guid:
        guid = entry.link
    elif entry.title:
        guid = entry.title

    return entry.get('id', guid)


def guids(entries, feed_has_no_guid=False):
    """
    return a list of all GUIDs of posts in list of entries.
    """
    guids = []
    for entry in entries:
        guids.append(entry_guid(entry, feed_has_no_guid))
    return guids


def entry_process(feedid, entry, postdict):
    """
    Receive Entry, process

    ..arguments:
        feed: feed-ID
        entry: actual Entry
        postdict: ?

    entry has these keys: (Spiegel.de)
     - 'summary_detail'
     - 'published'
     - 'published_parsed'
     - 'links'
     - 'title'
     - 'tags'
     - 'summary'
     - 'content'
     - 'guidislink'
     - 'title_detail'
     - 'link'
     - 'id'

    returnvalue::
         Either ENTRY_NEW
    """

    logger.debug("start: entry-processing")
    logger.info("feed-id: %s", feedid)
    logger.info("entry: %s", str(entry)[:40])
    logger.info("postdict: %s", postdict)

    result = ENTRY_SAME

    feed = Feed.objects.get(pk=feedid)

    p, created = Post.objects.get_or_create(
        feed=feed,
        title=entry.title,
        guid=entry_guid(entry, feed.has_no_guid),
    )

    if created:
        result = ENTRY_NEW
        logger.debug(
            "'%s' is a new entry for feed %s (%s)",
            entry.title,
            feed.id,
            p.id
        )
        p.content = entry.content
        p.published = datetime.datetime.utcfromtimestamp(
            calendar.timegm(entry.published_parsed)
        )
        p.save()
        logger.info(
            "Saved '%s', new entry for feed %s (%s)",
            entry.title,
            feed.id,
            p.id
        )

    if hasattr(entry, 'link'):
        if p.link is not entry.link:
            p.link = entry.link
            if not created:
                result = ENTRY_UPDATED

    logger.debug("stop: entry")
    p.save()
    return result


def feed_parse(feed):
    """
    Parse feed and catch the most common problems
    """
    try:
        fpf = feedparser.parse(
            feed.feed_url,
            agent=USER_AGENT,
            etag=feed.etag
        )
    except Exception as e:
        logger.error(
            'Feedparser Error: (%s) cannot be parsed: %s',
            feed.feed_url,
            str(e)
        )
        raise e

    if 'status' not in fpf or fpf.status >= 400:
        raise FeedErrorHTTP

    if 'bozo' in fpf and fpf.bozo == 1:
        logger.error(
            "[%d] !BOZO! Feed is not well formed: %s",
            feed.id,
            feed.name
        )
        raise FeedErrorParse

    if fpf.status == 304:
        logger.debug(
            "[%d] Feed did not change: %s",
            feed.id,
            feed.name
        )
        raise FeedSame

    logger.debug("-- end --")
    return fpf


def feed_update(feed, parsed):
    """
    Update `feed` with values from `parsed`
    """
    feed.etag = parsed.get('etag', '')
    feed.pubdate = parsed.feed.get('pubDate', '')
    print("%s" % (feed.pubdate))
    feed.last_modified = datetime.datetime.utcfromtimestamp(
        calendar.timegm(
            parsed.feed.get('updated_parsed', feed.pubdate)
        )
    )
    feed.title = parsed.feed.get('title', '')[0:254]
    feed.tagline = parsed.feed.get('subtitle', '')
    feed.link = parsed.feed.get('link', '')
    feed.language = parsed.feed.get('language', '')
    feed.copyright = parsed.feed.get('copyright', '')
    feed.author = parsed.feed.get('author', '')
    feed.webmaster = parsed.feed.get('webmaster', '')

    feed.save()
    return feed


def feed_postdict(feed, uids):
    """
    fetch posts that we have on file already and return a dictionary
    with all uids/posts as key/value pairs.
    """
    all_posts = Post.objects.filter(feed=feed)
    postdict = dict(
        [(post.guid, post) for post in all_posts.filter(
            guid__in=uids
        )]
    )
    return postdict


@shared_task
def feed_refresh_stats(result_list, feed_id):
    """
    this function is supposed to collect all the return
    values from `entry_process`. That function will return either:
        ENTRY_NEW
        ENTRY_UPDATED
        ENTRY_SAME
        ENTRY_ERR
    """
    result = {
        ENTRY_NEW: 0,
        ENTRY_UPDATED: 0,
        ENTRY_SAME: 0,
        ENTRY_ERR: 0
    }
    result.update(Counter(result_list))
    stat = FeedEntryStats()
    stat.feed = Feed.objects.get(pk=feed_id)
    stat.entry_new = result[ENTRY_NEW]
    stat.entry_same = result[ENTRY_SAME]
    stat.entry_updated = result[ENTRY_UPDATED]
    stat.entry_err = result[ENTRY_ERR]
    stat.save()
    return result


@shared_task
def feed_refresh(feed_id):
    """
    refresh entries for `feed_id`

    .. todo:: returns `FEED_OK`

    This should return either:
    `FEED_OK`: for any feed that was processed without an issue.
    `FEED_SAME`: for any feed that did not have an update.
    `FEED_ERRPARSE`: for any feed that could not be parsed.

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    logger.debug("-- start --")

    feed = Feed.objects.get(pk=feed_id)

    try:
        parsed = feed_parse(feed)
    except FeedErrorHTTP as e:
        return FEED_ERRHTTP
    except FeedErrorParse as e:
        return FEED_ERRPARSE(e)
    except FeedSame:
        return FEED_SAME

    feed = feed_update(feed, parsed)

    guid_list = guids(parsed.entries)
    postdict = feed_postdict(feed, guid_list)

    try:
        result = Counter(
            (
                entry_process(feed, entry, postdict)
                for
                entry
                in
                parsed.entries
            )
        )
    except SoftTimeLimitExceeded as timeout:
        logger.info("SoftTimeLimitExceeded: %s", timeout)
        logger.debug("-- end (ERR) --")
        return FEED_ERREXC
    except Exception as e:
        logger.debug("-- end (ERR) --")
        raise e
        return FEED_ERREXC

    logger.info(
        "Feed '%s' returned %s",
        feed.title,
        result
    )
    logger.debug("-- end --")
    return FEED_OK
