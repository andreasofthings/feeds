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
from celery import chord
from datetime import datetime, timedelta
from xml.dom.minidom import parseString

# from exceptions import ValidationError

from django.template.defaultfilters import slugify
from django.conf import settings

from feeds.piwik import Piwik

from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC

from feeds.tools import mtime, prints, getText
from feeds.models import Feed, Post, Tag, Category, TaggedPost

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

@celery.task(time_limit=10)
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

    if resp.has_key('status') and resp['status'] == "200":
        result = simplejson.loads(content)
        entry.tweets = result['count']
        entry.save()
    else:
        logger.debug("status error: %s: %s", resp, content)

    logger.debug("stop: counting tweets. got %s", entry.tweets)
    return entry.tweets

@celery.task(time_limit=10)
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

    logger.debug("stop: counting facebook shares & likes. got %s shares and %s likes.", entry.shares, entry.likes)
    return True

@celery.task(time_limit=10)
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
    headers = {'Content-type': 'application/json',}

    resp, content = http.request(
        queryurl, 
        method="POST", 
        body=simplejson.dumps(params), 
        headers=headers
    )

    if resp.has_key('status') and resp['status'] == "200":
        result = simplejson.loads(content)
        try:
            plusone = int( result['result']['metadata']['globalCounts']['count'] )
            entry.plus1 = plusone
            entry.save()
            logger.debug("stop: counting +1s. Got %s.", plusone)
            return plusone
        except KeyError, e:
            raise KeyError, e
    else:
        logger.debug("stop: counting +1s. Got none. or something weird happened.")

@celery.task(time_limit=10)
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
    pageurl = "http://angry-planet.com%s"%(entry.get_absolute_url())
    entry.pageviews = piwik.getPageActions(pageurl)
    entry.save()
    logger.debug("stop: get local pageviews. got %s.", entry.pageviews)
    return entry.pageviews

@celery.task
def tsum(numbers):
    return sum(numbers)

@celery.task
def entry_update_social(entry_id):
    logger = logging.getLogger(__name__)

    logger.debug("start: social scoring")

    if not entry_id:
        logger.error("can't get tags for non-post. pk is empty.")
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

    logger.debug("stop: social scoring. got %s"%p.score)
    return p.score


@celery.task
def entry_tags(entry_id, tags):
    """
    Process tags for entry.
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: entry tags: %s", tags)
    
    if not entry_id:
        logger.error("can't get tags for non-post. pk is empty.")
        return

    entry = Post.objects.get(pk=entry_id)

    if tags is not "":
        if isinstance(tags, types.ListType):
            for tag in tags:
                t, created = Tag.objects.get_or_create(name=str(tag.term), slug=slugify(tag.term))
                if created:
                    t.save()
                tp, created = TaggedPost.objects.get_or_create(tag=t, post=entry)
                if created:
                    tp.save()
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
    
    if hasattr(entry, 'link'):
        p.link = entry.link

    if hasattr(entry, 'content'):
        p.content = entry.content[0].value

    p.save()

    entry_update_social.delay(p.id)

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
    job.delay()
    logger.debug("stop aggregating")
    return True

