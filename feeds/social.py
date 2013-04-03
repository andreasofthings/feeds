#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
social tasks for angry planet

"""

import time, datetime, traceback, sys
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import simplejson
from django.http import HttpRequest
from django.contrib.auth.models import User
import twitter
from piwik import Piwik

POST_OK, POST_FAIL, POST_ERREXC = range(3)
from feeds.tools import prints, getText

import httplib2
import urllib
from xml.dom.minidom import parseString

try:
    import threadpool
except ImportError:
    threadpool = None

class SocialException(Exception):
    """
    Exception thrown by social functions
    """
    pass


class ProcessSocial:
    """
    get social stats for post
    """
    post = None

    def __init__(self, post):
        assert(post)
        self.http = httplib2.Http()
        self.post = post
        self.link = self.post.link.split("#")[0]

        self.piwik = Piwik() 
        self.twitter = twitter.Api()
        self.domain = Site.objects.get(id=settings.SITE_ID)

    def _update_twitter(self):
        """
        count tweets
        
        this is the old implementation 
        it is deprecated
        the new version lives in tasks.py
        """
        twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
        query = twitter_count % (self.link)

        resp, content = self.http.request(query, "GET")

        if resp.has_key('status') and resp['status'] == "200":
            result = simplejson.loads(content)
        else:
            print resp, content
   
        return result['count']

    def _update_facebook(self):
        """
        shares & likes
        """
        # facebook
        # https://api.facebook.com/method/fql.query?query=
        # select%20%20like_count,%20total_count,%20share_count,%20click_count%20from%20link_stat%20where%20url=%22http://www.saschakimmel.com/2010/05/how-to-capture-clicks-on-the-facebook-like-button/%22
        facebook_sql = """select like_count, share_count from link_stat where url='%s'"""
        query_sql = facebook_sql % (self.link)
        facebook_api = "https://api.facebook.com/method/fql.query?query=%s"
        query_url = facebook_api % (urllib.quote(query_sql))

        resp, content = self.http.request(query_url, "GET")

        if resp.has_key('status') and resp['status'] == "200":
            xml = parseString(content)
            for i in xml.getElementsByTagName("link_stat"):
                for j in i.getElementsByTagName("like_count"):
                    likes = int(getText(j.childNodes))
                for j in i.getElementsByTagName("share_count"):
                    shares = int(getText(j.childNodes))

        return likes, shares

    def _update_plus1(self):
        """
        plus 1
        """
        queryurl = "https://clients6.google.com/rpc"
        params = {
            "method": "pos.plusones.get",
            "id": "p",
            "params": {
                "nolog": True,
                "id": "%s" % (self.link),
                "source": "widget",
                "userId": "@viewer",
                "groupId": "@self",
            },
            "jsonrpc": "2.0",
            "key": "p",
            "apiVersion": "v1"
        }
        headers = {'Content-type': 'application/json',}

        resp, content = self.http.request(
                queryurl, 
                method="POST", 
                body=simplejson.dumps(params), 
                headers=headers
            )

        if resp.has_key('status') and resp['status'] == "200":
            result = simplejson.loads(content)
            return int( result['result']['metadata']['globalCounts']['count'] )
        else:
            print resp, content
  
    def _update_piwik(self):
        """
        get pageviews from tracking
        """
        pageurl = "http://%s%s"%(self.domain, self.post.get_absolute_url())
        # v = self.piwik.getPageVisits(pageurl)
        self.post.pageviews = self.piwik.getPageActions(pageurl)

    def process(self):
        retval = POST_OK

        try:
            # twitter
            self.post.tweets = self._update_twitter()
        except Exception, error:
            raise SocialError(error)

        try:
            # facebook
            self.post.likes, self.post.shares = self._update_facebook()
        except Exception, e:
            raise SocialError(e)

        try:
            # google+1
            self.post.plus1 = self._update_plus1()
        except Exception, e:
            raise SocialError(e)

        # calculate "social score"
        self.post.score = self.post.tweets + self.post.likes + self.post.shares + self.post.plus1 + self.post.blogs + self.post.pageviews

        # remember this was updated
        self.post.updated_social = True
        self.post.save()

        # self._update_piwik()
        #  self._update_twitter()
        # self.post.updated_social = True
        # self.post.save()
        return retval


class Dispatcher:
    def __init__(self, options, num_threads):
        self.options = options
        self.post_stats = {
            POST_OK:0,
            POST_FAIL:0,
            POST_ERREXC:0,
            }
        self.post_trans = {
            POST_OK:'ok',
            POST_FAIL:'fail',
            POST_ERREXC:'error',
            }
        self.post_keys = sorted(self.post_trans.keys())
        if threadpool:
            self.tpool = threadpool.ThreadPool(num_threads)
        else:
            self.tpool = None
        self.time_start = datetime.datetime.now()


    def add_job(self, post):
        """ adds a post processing job to the pool
        """
        if self.tpool:
            req = threadpool.WorkRequest(self.process_social_wrapper,
                (post,))
            self.tpool.putRequest(req)
        else:
            # no threadpool module, just run the job
            self.process_social_wrapper(post)

    def process_social_wrapper(self, post):
        """ wrapper for ProcessSocialPost
        """
        start_time = datetime.datetime.now()
        try:
            psocial = ProcessSocial(post, self.options)
            ret_social, ret_entries = psocial.process()
            del psocial
        except:
            (etype, eobj, etb) = sys.exc_info()
            print '[%d] ! -------------------------' % (post.id,)
            print traceback.format_exception(etype, eobj, etb)
            traceback.print_exception(etype, eobj, etb)
            print '[%d] ! -------------------------' % (post.id,)
            ret_social = POST_ERREXC
            ret_entries = {}

        delta = datetime.datetime.now() - start_time
        # todo: make this configureable
        if delta.seconds > 10:
            comment = u' (SLOW UPDATE!)'
        else:
            comment = u''
#        prints(u'[%d] Processed %s in %s [%s] [%s]%s' % (
#            feed.id, feed.feed_url, unicode(delta),
#            self.feed_trans[ret_feed],
#            u' '.join(u'%s=%d' % (self.entry_trans[key],
#                      ret_entries[key]) for key in self.entry_keys),
#            comment))

#        self.feed_stats[ret_feed] += 1
#        for key, val in ret_entries.items():
#            self.entry_stats[key] += val

        return 0, 0 # ret_feed, ret_entries 

    def poll(self):
        """ polls the active threads
        """
        if not self.tpool:
            # no thread pool, nothing to poll
            return
        while True:
            try:
                time.sleep(0.2)
                self.tpool.poll()
            except KeyboardInterrupt:
                prints('! Cancelled by user')
                break
            except threadpool.NoResultsPending:
                prints(u'* DONE in %s\n* Feeds: %s\n* Entries: %s' % (
                    unicode(datetime.datetime.now() - self.time_start),
                    u' '.join(u'%s=%d' % (self.feed_trans[key],
                              self.feed_stats[key])
                              for key in self.feed_keys),
                    u' '.join(u'%s=%d' % (self.entry_trans[key],
                              self.entry_stats[key])
                              for key in self.entry_keys)
                    ))
                break







def update():
    # ToDo:
    # should be done threaded, handled by Dispatcher below...
    from feeds.models import Post
    one_hour_ago = datetime.datetime.now()-datetime.timedelta(0,3600,0)

    p = Post.objects.filter(updated_social=False).order_by('-created').filter(created__gte=one_hour_ago)
    for i in p:
        processor = ProcessSocial(i)
        try:
            processor.process()
        except Exception, e:
            print str(e)

    # from social import Dispatcher
    #posts = Post.objects.filter(updated_social=False)
    #class Options:
    #  verbose = False

    #options = Options()
 
    #disp = Dispatcher(options, 25) 
    #for post in posts:
    #  disp.add_job(post)

