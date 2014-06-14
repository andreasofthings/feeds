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
import types
import httplib2
import simplejson
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

from feeds.piwik import Piwik

from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC

from feeds.tools import mtime, getText
from feeds.models import Feed, Post, Tag, TaggedPost
from feeds.models import FeedStats, FeedEntryStats


@shared_task
def dummy(x=10, *args, **kwargs):
    """
    Dummy celery.task that sleeps for x seconds,
    where the default for x is 10
    it returns True
    """
    from time import sleep
    logger = logging.getLogger(__name__)
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
    logger = logging.getLogger(__name__)
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
    logger = logging.getLogger(__name__)
    logger.debug("start: counting tweets")

    if not entry_id:
        logger.error("can't count tweets for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)
    http = httplib2.Http()
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (entry.link)

    resp, content = http.request(query, "GET")

    if 'status' in resp and resp['status'] == "200":
        result = simplejson.loads(content)
        entry.tweets = result['count']
        entry.save()
    else:
        logger.debug("status error: %s: %s", resp, content)

    logger.debug("stop: counting tweets. got %s", entry.tweets)
    return entry.tweets


@shared_task(time_limit=10)
def entry_update_facebook(entry_id):
    """
    count facebook shares & likes
    """
    logger = logging.getLogger(__name__)

    if not entry_id:
        logger.error("can't count shares&likes for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)
    logger.debug("start: facebook shares & likes for %s...", entry.guid)
    fb_api = "https://api.facebook.com/method/fql.query?query=%s"
    fb_sql = """select like_count, share_count from link_stat where url='%s'"""
    query_sql = fb_sql % (entry.link)
    query_url = fb_api % (quote(query_sql))
    http = httplib2.Http()
    resp, content = http.request(query_url, "GET")

    if 'status' in resp and resp['status'] == "200":
        xml = parseString(content)
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
    logger = logging.getLogger(__name__)
    logger.debug("start: counting +1s")

    if not entry_id:
        logger.error("can't count +1s for non-post. pk is empty.")
        return

    http = httplib2.Http()
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

    resp, content = http.request(
        queryurl,
        method="POST",
        body=simplejson.dumps(params),
        headers=headers
    )

    if 'status' in resp and resp['status'] == "200":
        result = simplejson.loads(content)
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


@shared_task(time_limit=10)
def entry_update_pageviews(entry_id):
    """
    get pageviews from piwik
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: get local pageviews")

    if not entry_id:
        logger.error("can't get local pageviews for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)

    piwik = Piwik()
    pageurl = "http://angry-planet.com%s" % (entry.get_absolute_url())
    entry.pageviews = piwik.getPageActions(pageurl)
    entry.save()
    logger.debug("stop: get local pageviews. got %s.", entry.pageviews)
    return entry.pageviews


@shared_task
def tsum(numbers):
    return sum(numbers)


@shared_task
def entry_update_social(entry_id):
    logger = logging.getLogger(__name__)

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
    if settings.FEED_POST_UPDATE_PAGEVIEWS:
        f = (entry_update_pageviews.subtask((p.id, )))
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
    """
    logger = logging.getLogger(__name__)
    logger.info("start: entry tagging (%s)", post_id)
    if not post_id:
        logger.error("Cannot tag Post (%s)", post_id)
        return
    p = Post.objects.get(pk=post_id)
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
    """

    logger = logging.getLogger(__name__)
    logger.debug("start: entry")
    feed = Feed.objects.get(pk=feed_id)
    logger.debug("Keys in entry '%s': %s", entry.title, entry.keys())

    p, created = Post.objects.get_or_create(
        feed=feed,
        title=entry.title,
        guid=get_entry_guid(entry, feed_id),
        published=True
    )

    if created:
        p.save()
        logger.debug("'%s' is a new entry (%s)", entry.title, p.id)

    if hasattr(entry, 'link'):
        p.link = entry.link

    if hasattr(entry, 'content'):
        p.content = entry.content[0].value

    p.save()

    if settings.FEED_POST_SOCIAL:
        entry_update_social.apply_async((p.id,), countdown=2)

    if created and 'tags' in entry:
        entry_tags.apply_async((p.id, entry['tags'],), countdown=2)

    if created and p.feed.announce_posts:
        twitter_post.apply_async((p.id,), countdown=2)

    logger.debug("stop: entry")
    return True


def feed_stats(result_list):
    """
    this function is supposed to collect all the return
    values from `entry_process`. That function will return either:
        ENTRY_NEW
        ENTRY_UPDATED
        ENTRY_SAME
        ENTRY_ERR
    """
    from collections import Counter
    feed_stats = {
        ENTRY_NEW: 0,
        ENTRY_UPDATED: 0,
        ENTRY_SAME: 0,
        ENTRY_ERR: 0
    }
    result = feed_stats.update(Counter(result_list))
    return result


@shared_task
def feed_refresh(feed_id):
    """
    refresh entries for `feed_id`

    .. todo:: returns `FEED_OK`

    saves :py:mod:`feeds.models.FeedEntryStats`

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

    if hasattr(fpf, 'status'):
        if fpf.status == 304:
            # this means feed has not changed
            return FEED_SAME
        if fpf.status >= 400:
            # this means a server error
            return FEED_ERRHTTP

    if hasattr(fpf, 'bozo') and fpf.bozo:
        logger.debug(
            "[%d] !BOZO! Feed is not well formed: %s",
            feed.id,
            feed.name
        )
        return FEED_ERRPARSE

    feed.etag = fpf.get('etag', '')
    feed.last_modified = mtime(fpf.modified)
    feed.title = fpf.feed.get('title', '')[0:254]
    feed.tagline = fpf.feed.get('tagline', '')
    feed.link = fpf.feed.get('link', '')
    feed.last_checked = datetime.now()
    guids = get_guids(fpf.entries)

    try:
        feed.save()
    except Feed.last_modified.ValidationError as e:
        logger.warning("Feed.ValidationError: %s", str(e))

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

    for entry in fpf.entries:
        try:
            # feed_id, options, entry, postdict, fpf
            logger.debug("spawning task: %s %s" % (entry.title, feed_id))
            r = chord(entry_process(
                entry,
                feed_id,
                postdict,
                fpf
            ), feed_stats.s())()
            FeedEntryStats(feed_id, r).save()
        except Exception as e:
            logger.debug("could not spawn task: %s" % (str(e)))

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
    Callback function for the `chord` in :py:mod:`feeds.tasks.aggregate`.

    Input: `result_list` will be a list of values from enum(FEED)

    Summarize the number of values and store into a dict.
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
    return result


@shared_task
def aggregate():
    """
    aggregate feeds

    type: celery task

    find all tasks that are marked for beta access

    returns a result_dict (FEED_OK/FEED_SAME/FEED_ERR), that
    comes from :py:mod:`feeds.tasks.aggregate_stats`

    .. codeauthor:: Andreas Neumeier
    """
    logger = logging.getLogger(__name__)
    feeds = Feed.objects.filter(is_active=True)
    logger.debug("processing %s feeds", feeds.count())
    return chord(
        (feed_refresh.s(i.id) for i in feeds),
        aggregate_stats.s()
    )()


def cronjob():
    job = aggregate.delay()
    result = job.get()
    fr = FeedStats(result)
    fr.save()
