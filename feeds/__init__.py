#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
.. testsetup:: *

   import feeds

The feeds module provides feed aggregation,
subscription, social ranking and stats.

:Author:    Andreas Neumeier
:Contact:   andreas@neumeier.org
:Version:   |version|
:Date:      |today|
:Copyright: BSD alike.

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

.. testcode::
  feeds.__version__ == "0.9.7"

.. testoutput::
  True

.. _Django: http://www.djangoproject.com
.. _Chartjs: http://www.chartjs.org

"""


default_app_config = 'feeds.apps.FeedsConfig'

version_info = (0, 9, 7)
__version__ = ".".join(map(str, version_info))
SERVER_SOFTWARE = "feeds/%s" % __version__


USER_AGENT = ""

ENTRY_NEW = u'entry_new'
ENTRY_UPDATED = u'entry_updated'
ENTRY_SAME = u'entry_same'
ENTRY_ERR = u'entry_err'

FEED_OK = u'feed_ok'
FEED_SAME = u'feed_same'
FEED_ERRPARSE = u'feed_errparse'
FEED_ERRHTTP = u'feed_errhttp'
FEED_ERREXC = u'feed_errexc'

CRON_OK = 'cron_ok'
CRON_FAIL = 'cron_fail'
CRON_ERR = 'cron_err'
CRON_RES = 'cron_res'
