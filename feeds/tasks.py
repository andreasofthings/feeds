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
import json

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
from celery.exceptions import SoftTimeLimitExceeded

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings

from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from feeds import CRON_OK, CRON_ERR

from .tools import getText
from .models import Feed, Post, Tag, TaggedPost
from .models import FeedStats

from exceptions import Exception


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
def aggregate_stats(result_list):
    """
    Callback function for the `chord` in :py:mod:`feeds.tasks.cronjob`.

    Input::
      `result_list` will be a list of values from enum(FEED)
      It will list all results from :py:mod:`feeds.tasks.feed_refresh`

    Summarize the number of values and store into a dict. For later
    the result is stored in :py:mod:`feeds.models.FeedStats`.
    """
    logger.debug("-- started --")
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
    logger.debug("-- end --")
    return result


@shared_task
def feed_refresh(pk):
    """
    Wrap Feed.refresh() to allow async execution in Celery.
    """
    return Feed.objects.get(pk=pk).refresh()


@shared_task
def cronjob():
    """
    aggregate feeds

    type: celery task

    Find all feeds.

    Returns a CRON_OK for no problems.
    Returns CRON_ERR when a problem occured.

    .. codeauthor:: Andreas Neumeier
    """
    logger.debug("-- started --")
    result = {}
    try:
        max_feeds = 1
        feeds = Feed.objects.filter(
            is_active=True
            ).filter(
                errors__lte=3
            ).filter(
                last_checked__eq=None
            )[:max_feeds]
        if feeds is None:
            feeds = Feed.objects.filter(
                is_active=True
                ).filter(
                    errors__lte=3
                ).order_by(
                    'last_checked'
                    )[:max_feeds]
        result = chord(
            (feed_refresh.s(i.id) for i in feeds),
            aggregate_stats.s()
        )()
    except SoftTimeLimitExceeded as timeout:
        logger.info("SoftTimeLimitExceeded: %s", timeout)
    except Exception, e:
        logger.error("Exception: %s", str(e))
        return CRON_ERR
    logger.debug("-- end --")
    return CRON_OK
