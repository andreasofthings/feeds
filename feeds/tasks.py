#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
async tasks, run via celery

updated to work with celery3
"""

import logging
import types
import twitter
import httplib2
import simplejson
import feedparser
import urllib
import celery
from datetime import datetime, timedelta
from xml.dom.minidom import parseString

# from exceptions import ValidationError

from django.template.defaultfilters import slugify
from django.conf import settings


from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC

from feeds.tools import mtime
from feeds.models import Feed, Post, Tag, Category

def get_entry_guid(entry, feed_id=None):
    """
    Get an individual guid for an entry
    """
    guid = None
    if entry.get('id', ''):
        guid = entry.get('id', '')
    elif entry.link:
        guid = entry.link
    elif entry.title:
        guid = entry.title

    if feed_id and not guid:
        feed = Feed.objects.get(pk=feed_id)
        guid = feed.link

    return entry.get('id', guid)


@celery.task
def dummy(x=10, *args, **kwargs):
    """
    Dummy celery.task that sleeps for x seconds,
    where the default for x is 10
    it returns True
    """
    from time import sleep
    logger = logging.getLogger(__name__)
    if kwargs.has_key('invocation_time'):
        logger.debug("task was delayed for %s", (datetime.now()-kwargs['invocation_time']))
    logger.debug("Started to sleep for %ss", x)
    sleep(x)
    logger.debug("Woke up after sleeping for %ss", x)
    return True

@celery.task
def entry_update_facebook(entry_id):
    """
    count facebook shares & likes
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: counting facebook shares & likes")
    entry = Post.objects.get(pk=entry_id)
    facebook_api = "https://api.facebook.com/method/fql.query?query=%s"
    facebook_sql = """select like_count, share_count from link_stat where url='%s'"""
    query_sql = facebook_sql % (entry.link)
    query_url = facebook_api % (urllib.quote(query_sql))
    http = httplib2.Http()
    resp, content = http.request(query_url, "GET")


    if resp.has_key('status') and resp['status'] == "200":
        xml = parseString(content)
        for i in xml.getElementsByTagName("link_stat"):
            for j in i.getElementsByTagName("like_count"):
                entry.likes = int(getText(j.childNodes))
            for j in i.getElementsByTagName("share_count"):
                entry.shares = int(getText(j.childNodes))

    entry.save()

    logger.debug("stop: counting facebook shares & likes")
    return True


@celery.task
def entry_update_twitter(entry_id):
    """
    count tweets
    
    this is the old implementation 
    it is deprecated
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: counting tweets")

    entry = Post.objects.get(pk=entry_id)
    http = httplib2.Http()
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (entry.link)

    resp, content = http.request(query, "GET")

    if resp.has_key('status') and resp['status'] == "200":
        result = simplejson.loads(content)
        entry.tweets = result['count']
        entry.save()
    else:
        logger.debug("status error: %s: %s", resp, content)

    logger.debug("stop: counting tweets")
    return True

@celery.task
def entry_tags(entry_id, tags):
    """
    Process tags for entry.
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: entry tags: %s", tags)
    
    entry = Post.objects.get(pk=entry_id)

    if tags is not "":
        if isinstance(tags, types.ListType):
            for tag in tags:
                t, created = Tag.objects.get_or_create(name=str(tag.term), slug=slugify(tag.term))
                if created:
                    t.save()
                entry.tags.add(t)
            entry.save()
    logger.debug("stop: entry tags")
    return

@celery.task
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
        logger.debug("'%s' is a new entry", entry.title)
        p.save()
    
    p.link = entry.link
    p.content = entry.content[0].value
    p.save()

    if settings.FEED_POST_UPDATE_TWITTER:
        entry_update_twitter.delay(p.id)
    if settings.FEED_POST_UPDATE_FACEBOOK:
        entry_update_facebook.delay(p.id)

    if entry.has_key('tags'):
        entry_tags.delay(p.id, entry.tags)

    logger.debug("stop: entry")
    return True

@celery.task
def feed_refresh(feed_id):
    """
    refresh entries for `feed_id`

    :codeauthor: Andreas Neumeier
    """
    logger = logging.getLogger(__name__)
    feed = Feed.objects.get(pk=feed_id)
    logger.debug("start")
    logger.info("collecting new posts for feed: %s (ID: %s)", feed.name, feed.id)

    feed_stats = { 
        ENTRY_NEW:0,
        ENTRY_UPDATED:0,
        ENTRY_SAME:0,
        ENTRY_ERR:0
    }

    try:
        fpf = feedparser.parse(feed.feed_url, agent=USER_AGENT, etag=feed.etag)
    except Exception, e: # Feedparser Exeptions
        logger.error('Feedparser Error: (%s) cannot be parsed: %s', feed.feed_url, str(e))
        
    if hasattr(fpf, 'status'):
        # feedparsere returned a status
        if fpf.status == 304:
            # this means feed has not changed
            logger.debug("%s (ID: %s) has not changed", feed.name, feed.id)
            return False
        if fpf.status >= 400:
            # this means a server error
            logger.debug("%s (ID: %s) gave a server error", feed.name, feed.id)
            return False
    if hasattr(fpf, 'bozo') and fpf.bozo:
        logger.debug("[%d] !BOZO! Feed is not well formed: %s", feed.id, feed.name)
        
    feed.etag = fpf.get('etag', '')

    # some times this is None (it never should) *sigh*
    if feed.etag is None:
        feed.etag = ''

    try:
        feed.last_modified = mtime(fpf.modified)
    except Exception, e:
        feed.last_modified = datetime.now()
        logger.debug("[%s] last_modified not well formed: %s Reason: %s", feed.name, feed.last_modified, str(e))
        
    feed.title = fpf.feed.get('title', '')[0:254]
    feed.tagline = fpf.feed.get('tagline', '')
    feed.link = fpf.feed.get('link', '')
    feed.last_checked = datetime.now()

    guids = []
    for entry in fpf.entries:
        guid = get_entry_guid(entry)
        guids.append(guid)

    try:
        feed.save()
    except Feed.last_modified.ValidationError, e:
        logger.warning("Feed.ValidationError: %s", str(e))


    if guids:
        """
        fetch posts that we have on file already
        """
        postdict = dict([(post.guid, post) for post in Post.objects.filter(feed=feed.id).filter(guid__in=guids)])
        logger.debug("postdict keys: %s", postdict.keys())
    else:
        """
        we didn't find any guids. leave postdict empty
        """
        postdict = {}

    for entry in fpf.entries:
        try:
            # feed_id, options, entry, postdict, fpf
            logger.debug("spawning task: %s %s"%(entry.title, feed_id)) # options are optional
            entry_process.delay(entry, feed_id, postdict, fpf) #options are optional
        except Exception, e:
            logger.debug("could not spawn task: %s"%(str(e)))

    feed.save()
    logger.debug("stop")
    return feed_stats

@celery.task
def aggregate():
    """
    aggregate feeds

    type: celery task

    find all tasks that are marked for beta access

    :codeauthor: Andreas Neumeier
    """
    from celery import group
    logger = logging.getLogger(__name__)
    logger.debug("start aggregating")
    feeds = Feed.objects.filter(is_active=True).filter(beta=True)
    logger.debug("processing %s feeds", feeds.count())
    job = group([feed_refresh.s(i.id) for i in feeds])
    job.apply_async()
    logger.debug("stop aggregating")
    return True

