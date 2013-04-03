#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
feeds is the core module for feedbrater.

feeds provides all functionality built from django methods, namely:
 
 - :mod:`feeds.models`
   the models to store information
 - :mod:`feeds.rss` 
   methods and classes to output re-build feeds
 - :mod:`feeds.views`
   the functions used to interface with the user
 - :mod:`feeds.forms`
   automated input handling through django-forms and crispy-forms
"""

USER_AGENT = ""
ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR = range(4)
FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC = range(5)

version_info = (0, 9, 1)
__version__ = ".".join(map(str, version_info))
SERVER_SOFTWARE = "feedbrater/%s" % __version__

# vim: ts=4 et sw=4 sts=4

