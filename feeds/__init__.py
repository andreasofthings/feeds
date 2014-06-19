#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
feeds - feed aggregator, social relevance and stats

:Author:    Andreas Neumeier
:Contact:   andreas@neumeier.org
:Revision:  $Revision: 1 $
:Date:      $Date: 2003-10-24 19:46:32 +0000 (Fri, 24 Oct 2003) $
:ID:        $Id:
:Copyright: To be decided soon. BSD alike, probably.

feeds is the core module for feeds.

feeds provides all functionality built on top of Django_ methods. Features
include aggregation of rss and Atom feeds, collection of social stats from
twitter, facebook, google+ and own piwik server, tracking of views in output
feeds (feedburner like), displaying all with Chartjs_.

 - :mod:`feeds.views`
 - :mod:`feeds.models`
 - :mod:`feeds.admin`
 - :mod:`feeds.forms`
 - :mod:`feeds.rss`

.. _Django: http://www.djangoproject.com
.. _Chartjs: http://www.chartjs.org

"""

USER_AGENT = ""
ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR = range(4)
FEED_OK = 'feed_ok'
FEED_SAME = 'feed_same'
FEED_ERRPARSE = 'feed_errparse'
FEED_ERRHTTP = 'feed_errhttp'
FEED_ERREXC = 'feed_errexc'

version_info = (0, 9, 6)
__version__ = ".".join(map(str, version_info))
SERVER_SOFTWARE = "feeds/%s" % __version__
