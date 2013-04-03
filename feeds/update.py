#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks!
feedjack & Gustavo Picón
"""

import os, time, datetime, traceback, sys
import feedparser

from django.conf import settings
from django.contrib.auth.models import User

from feeds.models import Feed, FeedPostCount, Post, Tag
from feeds.tools import encode, prints, mtime

try:
    import threadpool
except ImportError:
    threadpool = None

VERSION = '0.1'
URL = 'http://angry-planet.org/'
USER_AGENT = 'Angry Planet %s - %s' % (VERSION, URL)
SLOWFEED_WARNING = 10
ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR = range(4)
FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC = range(5)


from celery import Task

class ProcessEntryTask(Task):
    def __init__(self, feed, options, entry, postdict, fpf, **kwargs):
        self.feed = feed
        self.options = options
        self.entry = entry
        self.postdict = postdict
        self.fpf = fpf

    def get_tags(self):
        """ Returns a list of tag objects from an entry.
        """

        fcat = []
        if self.entry.has_key('tags'):
            for tcat in self.entry.tags:
                if tcat.label != None:
                    term = tcat.label
                else:
                    term = tcat.term
                qcat = term.strip()
                if ',' in qcat or '/' in qcat:
                    qcat = qcat.replace(',', '/').split('/')
                else:
                    qcat = [qcat]
                for zcat in qcat:
                    tagname = zcat.lower()
                    while '  ' in tagname:
                        tagname = tagname.replace('  ', ' ')
                    tagname = tagname.strip()
                    if not tagname or tagname == ' ':
                        continue
                    if not Tag.objects.filter(name=tagname):
                        cobj = Tag(name=tagname)
                        cobj.save()
                    fcat.append(Tag.objects.get(name=tagname))
        return fcat

    def get_entry_data(self):
        """ Retrieves data from a post and returns it in a tuple.
        """
        try:
            link = self.entry.link
        except AttributeError:
            link = self.feed.link
        try:
            title = self.entry.title
        except AttributeError:
            title = link
        guid = self.entry.get('id', title)

        if self.entry.has_key('author_detail'):
            author = self.entry.author_detail.get('name', '')
            author_email = self.entry.author_detail.get('email', '')
        else:
            author, author_email = '', ''

        if not author:
            author = self.entry.get('author', self.entry.get('creator', ''))
        if not author_email:
            # this should be optional~
            author_email = 'nospam@nospam.com'
        
        try:
            content = self.entry.content[0].value
        except:
            content = self.entry.get('summary',
                                     self.entry.get('description', ''))
        
        if self.entry.has_key('modified_parsed'):
            date_modified = mtime(self.entry.modified_parsed)
        else:
            date_modified = None

        fcat = self.get_tags()
        comments = self.entry.get('comments', '')

        return (link, title, guid, author, author_email, content, 
                date_modified, fcat, comments)
    def run(self, **kwargs):
        pass




class ProcessEntry:
    def __init__(self, feed, options, entry, postdict, fpf):
        self.feed = feed
        self.options = options
        self.entry = entry
        self.postdict = postdict
        self.fpf = fpf

    def get_tags(self):
        """ Returns a list of tag objects from an entry.
        """

        fcat = []
        if self.entry.has_key('tags'):
            for tcat in self.entry.tags:
                if tcat.label != None:
                    term = tcat.label
                else:
                    term = tcat.term
                qcat = term.strip()
                if ',' in qcat or '/' in qcat:
                    qcat = qcat.replace(',', '/').split('/')
                else:
                    qcat = [qcat]
                for zcat in qcat:
                    tagname = zcat.lower()
                    while '  ' in tagname:
                        tagname = tagname.replace('  ', ' ')
                    tagname = tagname.strip()
                    if not tagname or tagname == ' ':
                        continue
                    if not Tag.objects.filter(name=tagname):
                        cobj = Tag(name=tagname)
                        cobj.save()
                    fcat.append(Tag.objects.get(name=tagname))
        return fcat

    def get_entry_data(self):
        """ Retrieves data from a post and returns it in a tuple.
        """
        try:
            link = self.entry.link
        except AttributeError:
            link = self.feed.link
        try:
            title = self.entry.title
        except AttributeError:
            title = link
        guid = self.entry.get('id', title)

        if self.entry.has_key('author_detail'):
            author = self.entry.author_detail.get('name', '')
            author_email = self.entry.author_detail.get('email', '')
        else:
            author, author_email = '', ''

        if not author:
            author = self.entry.get('author', self.entry.get('creator', ''))
        if not author_email:
            # this should be optional~
            author_email = 'nospam@nospam.com'
        
        try:
            content = self.entry.content[0].value
        except:
            content = self.entry.get('summary',
                                     self.entry.get('description', ''))
        
        if self.entry.has_key('modified_parsed'):
            date_modified = mtime(self.entry.modified_parsed)
        else:
            date_modified = None

        fcat = self.get_tags()
        comments = self.entry.get('comments', '')

        return (link, title, guid, author, author_email, content, 
                date_modified, fcat, comments)

    def process(self):
        """ Process a post in a feed and saves it in the DB if necessary.
        """

        (link, title, guid, author, author_email, content, date_modified,
         fcat, comments) = self.get_entry_data()
        
        if False and self.options.verbose:
            prints(u'[%d] Entry\n' \
                   u'  title: %s\n' \
                   u'  link: %s\n' \
                   u'  guid: %s\n' \
                   u'  author: %s\n' \
                   u'  author_email: %s\n' \
                   u'  tags: %s' % (
                self.feed.id,
                title, link, guid, author, author_email,
                u' '.join(tcat.name for tcat in fcat)))

        if guid in self.postdict:
            tobj = self.postdict[guid]
            if tobj.content != content or (date_modified and
                    tobj.date_modified != date_modified):
                retval = ENTRY_UPDATED
                if self.options.verbose:
                    prints('[%d] Updating existing post: %s' % (
                           self.feed.id, link))
                if not date_modified:
                    # damn non-standard feeds
                    date_modified = tobj.date_modified
                tobj.title = title
                tobj.link = link
                tobj.content = content
                tobj.guid = guid
                tobj.date_modified = date_modified
                tobj.author = author
                tobj.author_email = author_email
                tobj.comments = comments
                tobj.tags.clear()
		# ToDo: Debug this properly
                try:
                  [tobj.tags.add(tcat) for tcat in fcat]
                except Exception, e:
                  print e
                tobj.save()
            else:
                retval = ENTRY_SAME
                if self.options.verbose:
                    prints('[%d] Post has not changed: %s' % (self.feed.id,
                                                              link))
        else:
            retval = ENTRY_NEW
            if self.options.verbose:
                prints('[%d] Saving new post: %s' % (self.feed.id, link))
            if not date_modified and self.fpf:
                # if the feed has no date_modified info, we use the feed
                # mtime or the current time
                if self.fpf.feed.has_key('modified_parsed'):
                    date_modified = mtime(self.fpf.feed.modified_parsed)
                elif self.fpf.has_key('modified'):
                    date_modified = mtime(self.fpf.modified)
            if not date_modified:
                date_modified = datetime.datetime.now()
            owner = User.objects.get(pk=1)
            tobj = Post(feed=self.feed, title=title, link=link,
                content=content, guid=guid, date_modified=date_modified,
                author=author, author_email=author_email,
                comments=comments, owner=owner)
	    # Ah, have to save and get an ID first
            tobj.save()
            [tobj.tags.add(tcat) for tcat in fcat]
            tobj.save()
        return retval


class ProcessFeed:
    def __init__(self, feed, options):
        self.feed = feed
        self.options = options
        self.fpf = None

    def process_entry(self, entry, postdict):
        """ wrapper for ProcessEntry
        """
        entry = ProcessEntry(self.feed, self.options, entry, postdict,
                             self.fpf)
        ret_entry = entry.process()
        del entry
        return ret_entry

    def process(self):
        """ Downloads and parses a feed.
        """

        ret_values = {
            ENTRY_NEW:0,
            ENTRY_UPDATED:0,
            ENTRY_SAME:0,
            ENTRY_ERR:0}

        prints(u'[%d] Processing feed %s' % (self.feed.id,
                                             self.feed.feed_url))

        # we check the etag and the modified time to save bandwith and
        # avoid bans
        try:
            self.fpf = feedparser.parse(self.feed.feed_url,
                                        agent=USER_AGENT,
                                        etag=self.feed.etag)
        except:
            prints('! ERROR: feed cannot be parsed')
            return FEED_ERRPARSE, ret_values
        
        if hasattr(self.fpf, 'status'):
            if self.options.verbose:
                prints(u'[%d] HTTP status %d: %s' % (self.feed.id,
                                                     self.fpf.status,
                                                     self.feed.feed_url))
            if self.fpf.status == 304:
                # this means the feed has not changed
                if self.options.verbose:
                    prints('[%d] Feed has not changed since ' \
                           'last check: %s' % (self.feed.id,
                                               self.feed.feed_url))
                return FEED_SAME, ret_values

            if self.fpf.status >= 400:
                # http error, ignore
                prints('[%d] !HTTP_ERROR! %d: %s' % (self.feed.id,
                                                     self.fpf.status,
                                                     self.feed.feed_url))
                return FEED_ERRHTTP, ret_values

        if hasattr(self.fpf, 'bozo') and self.fpf.bozo:
            prints('[%d] !BOZO! Feed is not well formed: %s' % (
                self.feed.id, self.feed.feed_url))

        # the feed has changed (or it is the first time we parse it)
        # saving the etag and last_modified fields
        self.feed.etag = self.fpf.get('etag', '')
        # some times this is None (it never should) *sigh*
        if self.feed.etag is None:
            self.feed.etag = ''

        try:
            self.feed.last_modified = mtime(self.fpf.modified)
        except:
            pass
        
        self.feed.title = self.fpf.feed.get('title', '')[0:254]
        self.feed.tagline = self.fpf.feed.get('tagline', '')
        self.feed.link = self.fpf.feed.get('link', '')
        self.feed.last_checked = datetime.datetime.now()

        if False and self.options.verbose:
            prints(u'[%d] Feed info for: %s\n' \
                   u'  title %s\n' \
                   u'  tagline %s\n' \
                   u'  link %s\n' \
                   u'  last_checked %s' % (
                self.feed.id, self.feed.feed_url, self.feed.title,
                self.feed.tagline, self.feed.link, self.feed.last_checked))

        guids = []
        for entry in self.fpf.entries:
            if entry.get('id', ''):
                guids.append(entry.get('id', ''))
            elif entry.title:
                guids.append(entry.title)
            elif entry.link:
                guids.append(entry.link)
        self.feed.save()
        if guids:
            postdict = dict([(post.guid, post) 
              for post in Post.objects.filter(
                   feed=self.feed.id).filter(guid__in=guids)])
        else:
            postdict = {}

        for entry in self.fpf.entries:
            try:
                ret_entry = self.process_entry(entry, postdict)
            except:
                (etype, eobj, etb) = sys.exc_info()
                print '[%d] ! -------------------------' % (self.feed.id,)
                print traceback.format_exception(etype, eobj, etb)
                traceback.print_exception(etype, eobj, etb)
                print '[%d] ! -------------------------' % (self.feed.id,)
                ret_entry = ENTRY_ERR
            ret_values[ret_entry] += 1

        self.feed.save()

        return FEED_OK, ret_values

class Dispatcher:
    def __init__(self, options, num_threads):
        self.options = options
        self.entry_stats = {
            ENTRY_NEW:0,
            ENTRY_UPDATED:0,
            ENTRY_SAME:0,
            ENTRY_ERR:0}
        self.feed_stats = {
            FEED_OK:0,
            FEED_SAME:0,
            FEED_ERRPARSE:0,
            FEED_ERRHTTP:0,
            FEED_ERREXC:0}
        self.entry_trans = {
            ENTRY_NEW:'new',
            ENTRY_UPDATED:'updated',
            ENTRY_SAME:'same',
            ENTRY_ERR:'error'}
        self.feed_trans = {
            FEED_OK:'ok',
            FEED_SAME:'unchanged',
            FEED_ERRPARSE:'cant_parse',
            FEED_ERRHTTP:'http_error',
            FEED_ERREXC:'exception'}
        self.entry_keys = sorted(self.entry_trans.keys())
        self.feed_keys = sorted(self.feed_trans.keys())
        if threadpool:
            self.tpool = threadpool.ThreadPool(num_threads)
        else:
            self.tpool = None
        self.time_start = datetime.datetime.now()


    def add_job(self, feed):
        """ adds a feed processing job to the pool
        """
        if self.tpool:
            req = threadpool.WorkRequest(self.process_feed_wrapper,
                (feed,))
            self.tpool.putRequest(req)
        else:
            # no threadpool module, just run the job
            self.process_feed_wrapper(feed)

    def process_feed_wrapper(self, feed):
        """ wrapper for ProcessFeed
        """
        start_time = datetime.datetime.now()
        try:
            pfeed = ProcessFeed(feed, self.options)
            ret_feed, ret_entries = pfeed.process()
            del pfeed
        except:
            (etype, eobj, etb) = sys.exc_info()
            print '[%d] ! -------------------------' % (feed.id,)
            print traceback.format_exception(etype, eobj, etb)
            traceback.print_exception(etype, eobj, etb)
            print '[%d] ! -------------------------' % (feed.id,)
            ret_feed = FEED_ERREXC
            ret_entries = {0:100, 1:100, 2:100, 3:100}

        delta = datetime.datetime.now() - start_time
        if delta.seconds > SLOWFEED_WARNING:
            comment = u' (SLOW FEED!)'
        else:
            comment = u''
        prints(u'[%d] Processed %s in %s [%s] [%s]%s' % (
            feed.id, feed.feed_url, unicode(delta),
            self.feed_trans[ret_feed],
            u' '.join(u'%s=%d' % (self.entry_trans[key],
                      ret_entries[key]) for key in self.entry_keys),
            comment))
        stats = FeedPostCount(
          feed=feed, 
          entry_new=ret_entries[ENTRY_NEW],
          entry_updated=ret_entries[ENTRY_UPDATED],
          entry_same=ret_entries[ENTRY_SAME],
          entry_err=ret_entries[ENTRY_ERR],
          )
        stats.save()

        self.feed_stats[ret_feed] += 1
        for key, val in ret_entries.items():
            self.entry_stats[key] += val

        return ret_feed, ret_entries

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
  # cleanup first
  # _cleanup()

  class Options:
    verbose = False

  options = Options()

  # get feeds due, maximum of 5 per cycle
  feeds = Feed.objects.filter(last_checked__lt=datetime.datetime.now()-datetime.timedelta(hours=1))[:5]
  feeds = Feed.objects.all()

  disp = Dispatcher(options, settings.FEEDS_WORKERTHREADS)
  for feed in feeds:
    disp.add_job(feed)

  disp.poll()

