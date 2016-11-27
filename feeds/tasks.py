#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:py:mod:`feeds.tasks`
=====================

Async tasks, run via celery, updated to work with celery3.

This module takes care of everything that is not client/customer facing.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from __future__ import absolute_import, unicode_literals

import logging
import types

try:
    from urllib.parse import urlparse
except ImportError:
    import urlparse

from datetime import datetime, timedelta

from celery import shared_task
from celery import chord
from celery.exceptions import SoftTimeLimitExceeded

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings

from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from feeds import CRON_OK, CRON_ERR

from .models import Feed, Post, TaggedPost
from .models import FeedStats
from .decorators import feedsocial

from category.models import Tag

from social.get import tweets, facebook, linkedin


logger = logging.getLogger(__name__)


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
def post_update_twitter(entry_id):
    """
    count tweets
    """
    import tweepy
    api = tweepy.API()

    if getattr(settings, 'FEEDS_POST_UPDATE_TWITTER', False):
        post = Post.objects.get(pk=entry_id)
        (post.tweets, ) = api.search(post.url)
        post.save()
        logger.debug("stop: counting tweets. got %s", post.tweets)
        return (post.tweets, )
    return (0, )


@shared_task(time_limit=10)
def post_update_facebook(entry_id):
    """
    count facebook
    """
    result = (-1, -1)
    if not entry_id:
        logger.error("Provided an invalid post_id")
        return result

    if getattr(settings, 'FEEDS_POST_UPDATE_FACEBOOK', False):
        post = Post.objects.get(pk=entry_id)
        (post.shares, post.likes, bla) = facebook(post)
        post.save()
        logger.debug(
            "stop: counting tweets. got %s shares and %s likes",
            post.shares,
            post.likes
        )
        return (post.shares, post.likes)
    return result


@shared_task(time_limit=10)
def post_update_linkedin(entry_id):
    """
    count linkedin
    """
    result = (-1, )
    if not entry_id:
        logger.error("Provided an invalid post_id")
        return result

    if getattr(settings, 'FEEDS_POST_UPDATE_LINKEDIN', False):
        post = Post.objects.get(pk=entry_id)
        (post.linkedin, ) = linkedin(post)
        post.save()
        logger.debug(
            "stop: counting linkedin. got %s",
            post.linkedin
        )
        return (post.linkedin, )
    return result


@shared_task
def tsum(numbers, post):
    """
    tsum
    ====
    This is a callback function and should never be invoked directly.
    """
    import itertools
    try:
        merged = list(itertools.chain.from_iterable(numbers))
    except TypeError as e:
        logger.error(e)
        logger.error(numbers)
        return 0

    post.score = sum(merged)
    post.save()


@shared_task
def post_update_social(post_id):

    logger.debug("start: social scoring")

    if getattr(settings, 'FEEDS_POST_UPDATE_SOCIAL', False):
        try:
            p = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            logger.debug("Post %s does not exist." % (post_id))
            return 0

        header = []

        f = (post_update_twitter.subtask((p.id, )))
        header.append(f)
        f = (post_update_facebook.subtask((p.id, )))
        header.append(f)
        f = (post_update_linkedin.subtask((p.id, )))
        header.append(f)

        callback = tsum.s(p)
        chord(header)(callback)

        logger.debug("stop: social scoring. got %s" % p.score)
        return p.score
    else:
        """
        Disabled, return 0.
        """
        return 0


@shared_task
def entry_tags(post_id, tags):
    """
    collect tags per post and do the postprocessing.
    """
    try:
        p = Post.objects.get(pk=post_id)
    except p.DoesNotExist:
        logger.error("Does not exist (%s)", post_id)
        return

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

    .. todo:: `py:mod:feeds.models.FeedStats` should rather accept the
              dict as input to map results correctly. Right now it picks all
              results from the dict explicitly.
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
def purge(ttl=timedelta(days=31)):
    """
    Removes posts older than `ttl`.

    returns True if OK
    returns False if not.
    """
    try:
        posts = Post.objects.older_than(ttl)
        posts.delete()
    except:
        return False
    return True


@shared_task
def cronjob():
    """
    aggregate feeds

    type: celery task

    Find all feeds.

    Returns a CRON_OK for no problems.
    Returns CRON_ERR when a problem occured.

    .. todo:: Only check feeds that have subscribers.

    .. codeauthor:: Andreas Neumeier
    """
    logger.debug("-- started --")
    result = {}
    max_feeds = 5
    qs = Feed.objects.filter(
        is_active=True
        ).filter(
            errors__lte=3
        )
    feeds = qs.filter(
        last_checked__isnull=True
        )
    if not feeds.exists():
        feeds = qs.order_by(
            'last_checked'
            )
    try:
        result = chord(
            (feed_refresh.s(i.id) for i in feeds[:max_feeds]),
            aggregate_stats.s()
        )()
    except SoftTimeLimitExceeded as timeout:
        logger.info("SoftTimeLimitExceeded: %s", timeout)
    except Exception as e:
        logger.error("Exception: %s", str(e))
        return CRON_ERR
    logger.debug("-- end (%s) -- " % result)
    return CRON_OK
