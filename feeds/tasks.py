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

import types
import requests

try:
    import json
except:
    import simplejson as json

import feedparser

try:
    from urllib.parse import urlparse
    from urllib.quote import quote
except ImportError:
    import urlparse
    from urllib import quote


from datetime import datetime
from xml.dom.minidom import parseString

from celery import shared_task
from celery import chord

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings

from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from feeds import CRON_OK, CRON_FAIL, CRON_ERR

from .tools import getText
from .models import Feed, Post, Tag, TaggedPost
from .models import FeedStats
from .models import FeedEntryStats


@shared_task
def dummy(x=10, *args, **kwargs):
    """
    Dummy celery.task that sleeps for x seconds,
    where the default for x is 10
    it returns True
    """
    from time import sleep

    if 'invocation_time' in kwargs:
        logger.debug(
            "task was delayed for %s",
            (datetime.now() - kwargs['invocation_time'])
        )
    logger.debug("Started to sleep for %ss", x)
    sleep(x)
    logger.debug("Woke up after sleeping for %ss", x)
    return True


def get_entry_guid(entry, feed_id=None):
    """
    Get an individual guid for an entry
    """
    guid = None
    feed = Feed.objects.get(pk=feed_id)

    if entry.get('id', ''):
        guid = entry.get('id', '')
    elif entry.link or feed.has_no_guid:
        guid = entry.link
    elif entry.title:
        guid = entry.title

    return entry.get('id', guid)


def get_guids(entries, feed_has_no_guid=False):
    """
    return a list of all GUIDs of posts in list of entries.
    """
    guids = []
    for entry in entries:
        guid = ""
        if entry.get('id', ''):
            guid = entry.get('id', '')
        elif entry.link or feed_has_no_guid:
            guid = entry.link
        elif entry.title:
            guid = entry.title
        guids.append(entry.get('id', guid))
    return guids


@shared_task
def twitter_post(post_id):
    """
    announce track and artist on twitter
    """
    logger.debug("twittering new post")
    if not post_id:
        """
        failed
        """
        return
    from twitter import Api
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(id=15)
    user_auth = user.social_auth.filter(provider="twitter")
    message = """%s on %s http://angry-planet.com%s""" % (
        post.title,
        post.feed.title,
        post.get_absolute_url()
    )
    for account in user_auth:
        access_token = urlparse.parse_qs(account.extra_data['access_token'])
        oauth_token = access_token['oauth_token'][0]
        oauth_access = access_token['oauth_token_secret'][0]
        twitter = Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=oauth_token,
            access_token_secret=oauth_access
        )
        result = twitter.PostUpdate(message)
        logger.debug("twitter said: %s", result)
    logger.debug("done twittering post")


@shared_task(time_limit=10)
def entry_update_twitter(entry_id):
    """
    count tweets

    """
    logger.debug("start: counting tweets")

    if not entry_id:
        logger.error("can't count tweets for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (entry.link)

    resp = requests.get(query)

    if resp.status_code == 200:
        result = json.loads(resp.text)
        entry.tweets = result['count']
        entry.save()
    else:
        logger.debug("status error: %s: %s", resp.status_code, resp.text)

    logger.debug("stop: counting tweets. got %s", entry.tweets)
    return entry.tweets


@shared_task(time_limit=10)
def entry_update_facebook(entry_id):
    """
    count facebook shares & likes
    """

    if not entry_id:
        logger.error("can't count shares&likes for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)
    logger.debug("start: facebook shares & likes for %s...", entry.guid)
    fb_api = "https://api.facebook.com/method/fql.query?query=%s"
    fb_sql = """select like_count, share_count from link_stat where url='%s'"""
    query_sql = fb_sql % (entry.link)
    query_url = fb_api % (quote(query_sql))
    resp = requests.get(query_url)

    if resp.status_code == 200:
        xml = parseString(resp.text)
        for i in xml.getElementsByTagName("link_stat"):
            for j in i.getElementsByTagName("like_count"):
                entry.likes = int(getText(j.childNodes))
            for j in i.getElementsByTagName("share_count"):
                entry.shares = int(getText(j.childNodes))

    entry.save()

    logger.debug("stop: facebook shares & likes. got %s shares and %s likes.",
                 entry.shares,
                 entry.likes
                 )
    return True


@shared_task(time_limit=10)
def entry_update_googleplus(entry_id):
    """
    plus 1
    """
    logger.debug("start: counting +1s")

    if not entry_id:
        logger.error("can't count +1s for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)

    queryurl = "https://clients6.google.com/rpc"
    params = {
        "method": "pos.plusones.get",
        "id": "p",
        "params": {
            "nolog": True,
            "id": "%s" % (entry.link),
            "source": "widget",
            "userId": "@viewer",
            "groupId": "@self",
        },
        "jsonrpc": "2.0",
        "key": "p",
        "apiVersion": "v1"
    }
    headers = {
        'Content-type': 'application/json',
    }

    resp, content = requests.post(
        queryurl,
        data=json.dumps(params),
        headers=headers
    )

    if resp.status_code == 200:
        result = json.loads(resp.text)
        try:
            entry.plus1 = int(
                result['result']['metadata']['globalCounts']['count']
            )
            entry.save()
            logger.debug("stop: counting +1s. Got %s.", entry.plus1)
            return entry.plus1
        except KeyError as e:
            raise KeyError(e)
    else:
        logger.debug("stop: counting +1s. Got none. Something weird happened.")


@shared_task
def tsum(numbers):
    return sum(numbers)


@shared_task
def entry_update_social(entry_id):

    logger.debug("start: social scoring")

    if not entry_id:
        logger.error("can't do social scoring for non-post. pk is empty.")
        return

    p = Post.objects.get(pk=entry_id)

    header = []

    if settings.FEED_POST_UPDATE_TWITTER:
        f = (entry_update_twitter.subtask((p.id, )))
        header.append(f)
    if settings.FEED_POST_UPDATE_FACEBOOK:
        f = (entry_update_facebook.subtask((p.id, )))
        header.append(f)
    if settings.FEED_POST_UPDATE_GOOGLEPLUS:
        f = (entry_update_googleplus.subtask((p.id, )))
        header.append(f)

    callback = tsum.s()
    result = chord(header)(callback)

    p.score = result.get(timeout=60)
    p.save()

    logger.debug("stop: social scoring. got %s" % p.score)
    return p.score


@shared_task
def entry_tags(post_id, tags):
    """
    collect tags per post and do the postprocessing.
    """
    if not post_id:
        logger.error("Cannot tag Post (%s)", post_id)
        return
    try:
        p = Post.objects.get(pk=post_id)
    except p.DoesNotExist:
        logger.error("Does not exist (%s)", post_id)

    logger.debug("start: entry tagging post '%s' (%s)", p.title, post_id)

    if tags is not "" and isinstance(tags, types.ListType):
        new_tags = 0
        for tag in tags:
            t, created = Tag.objects.get_or_create(
                name=str(tag.term),
                slug=slugify(tag.term)
            )
            if created:
                logger.info("created new tag '%s'", t)
                t.save()
                new_tags += 1
            tp, created = TaggedPost.objects.get_or_create(tag=t, post=p)
            if created:
                tp.save()
        p.save()
    logger.info("created %s new tags", new_tags)
    logger.debug("stop: entry tagging")


@shared_task
def entry_process(entry, feed_id, postdict, fpf):
    """
    Receive Entry, process

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

    feed = Feed.objects.get(pk=feed_id)

    logger.debug("start: entry-processing")
    logger.debug("Keys in entry '%s': %s", entry.title, entry.keys())

    result = ENTRY_SAME

    p, created = Post.objects.get_or_create(
        feed=feed,
        title=entry.title,
        guid=get_entry_guid(entry, feed_id),
        published=True
    )

    if created:
        p.save()
        logger.debug("'%s' is a new entry (%s)", entry.title, p.id)
        result = ENTRY_NEW

    if hasattr(entry, 'link'):
        if p.link is not entry.link:
            p.link = entry.link
            result = ENTRY_UPDATED

    if hasattr(entry, 'content'):
        if p.content is not entry.content[0].value:
            p.content = entry.content[0].value
            result = ENTRY_UPDATED

    p.save()

    if settings.FEEDS_POST_SOCIAL:
        entry_update_social.apply_async((p.id,), countdown=2)

    if created and 'tags' in entry:
        entry_tags.apply_async((p.id, entry['tags'],), countdown=2)

    if created and p.feed.announce_posts:
        twitter_post.apply_async((p.id,), countdown=2)

    logger.debug("stop: entry")
    return result


@shared_task
def feed_stats(result_list, feed_id):
    """
    this function is supposed to collect all the return
    values from `entry_process`. That function will return either:
        ENTRY_NEW
        ENTRY_UPDATED
        ENTRY_SAME
        ENTRY_ERR
    """
    from collections import Counter
    stats = {
        ENTRY_NEW: 0,
        ENTRY_UPDATED: 0,
        ENTRY_SAME: 0,
        ENTRY_ERR: 0
    }
    result = stats.update(Counter(result_list))
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
    logger = logging.getLogger(__name__)

    feed = Feed.objects.get(pk=feed_id)

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
        return FEED_ERRPARSE

    if 'status' not in fpf or fpf.status >= 400:
        return FEED_ERRHTTP

    if fpf.status is 304:
        logger.debug(
            "[%d] Feed did not change: %s",
            feed.id,
            feed.name
        )
        return FEED_SAME

    if 'bozo' in fpf and fpf.bozo == 1:
        logger.error(
            "[%d] !BOZO! Feed is not well formed: %s",
            feed.id,
            feed.name
        )
        return FEED_ERRPARSE

    feed.etag = fpf.get('etag', '')
    feed.last_modified = fpf.get('modified', '2000-01-01 00:00')
    feed.title = fpf.feed.get('title', '')[0:254]
    feed.tagline = fpf.feed.get('tagline', '')
    feed.link = fpf.feed.get('link', '')
    guids = get_guids(fpf.entries)

    if guids:
        """
        fetch posts that we have on file already
        """
        postdict = dict(
            [(post.guid, post) for post in Post.objects.filter(
                feed=feed.id
            ).filter(
                guid__in=guids
            )]
        )
        logger.debug("postdict keys: %s", postdict.keys())
    else:
        """
        we didn't find any guids. leave postdict empty
        """
        postdict = {}

    try:
        result = chord(
            (
                entry_process.s(
                    entry, feed.id, postdict, fpf
                )
                for entry in fpf.entries
            ),
            feed_stats.s(feed.id)
        )()
    except:
        return FEED_ERREXC
    """Chord to asynchronously process all entries in parsed feed."""

    feed.save()
    logger.info(
        "Feed '%s' had %s new entries",
        feed.title,
        feed_stats[ENTRY_NEW]
    )
    logger.debug("stop")
    return FEED_OK


@shared_task
def aggregate_stats(result_list):
    """
    Callback function for the `chord` in :py:mod:`feeds.tasks.cronjob`.

    Input::
      `result_list` will be a list of values from enum(FEED)
      It will list all results from :py:mod:`feeds.tasks.feed_refresh`

    Summarize the number of values and store into a dict. For later
    the result is stored in :py:mod:`feeds.models.FeedStats`.
    """
    from collections import Counter
    result = {
        FEED_OK: 0,
        FEED_SAME: 0,
        FEED_ERRPARSE: 0,
        FEED_ERRHTTP: 0,
        FEED_ERREXC: 0
    }
    result.update(Counter(result_list))
    """Add upp all fields in the `result_list`-argument."""
    stat = FeedStats()
    """
    New instance of `py:mod:feeds.models.FeedStats` to keep the result.
    ToDo: `py:mod:feeds.models.FeedStats` should rather
    accept the dict as input.
    """
    stat.feed_ok = result[FEED_OK]
    stat.feed_same = result[FEED_SAME]
    stat.feed_errparse = result[FEED_ERRPARSE]
    stat.feed_errhttp = result[FEED_ERRHTTP]
    stat.feed_errexc = result[FEED_ERREXC]
    stat.save()
    return result


@shared_task
def cronjob(max_feeds=0):
    """
    aggregate feeds

    type: celery task

    Find all tasks that are marked for beta access

    param:: max_feeds
      Check at most max_feeds

    Returns a CRON_OK for no problems.
    Returns CRON_ERR when a problem occured.

    .. codeauthor:: Andreas Neumeier
    """
    logger.debug("-- cronjob started --")
    result = {}
    try:
        feeds = Feed.objects.filter(is_active=True)
        if max_feeds > 0:
            feeds = feeds[:max_feeds]
        result = chord(
            (feed_refresh.s(i.id) for i in feeds),
            aggregate_stats.s()
        )()
    except Exception, e:
        logger.debug("Exception: %s", str(e))
        print e
        return CRON_ERR

    if (sum(result.values() == result[FEED_OK])):
        return CRON_OK
    else:
        return CRON_FAIL
