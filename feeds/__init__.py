#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
"""

USER_AGENT = ""
ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR = range(4)
FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC = range(5)

version_info = (0, 9, 1)
__version__ = ".".join(map(str, version_info))
SERVER_SOFTWARE = "feedbrater/%s" % __version__

# vim: ts=4 et sw=4 sts=4

