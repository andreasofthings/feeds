#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Exceptions.
"""

class FeedErrorHTTP(Exception):
    """
    Exception when Feed returns an HTTP Error
    """
    pass


class FeedErrorParse(Exception):
    """
    Exception when Feed could not be parsed.
    """
    pass


class FeedSame(Exception):
    """
    Exception when Feed hasn't changed since last time.
    """
    pass
