#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Exceptions.
"""

import logging
logger = logging.getLogger(__name__)


class FeedsBaseException(Exception):
    """Generic exception for `feeds`."""

    def __init__(self, msg, original_exception):
        super(FeedsBaseException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
        logger.debug(msg)


class FeedsHTTPError(FeedsBaseException):
    """
    Exception when Feed returns an HTTP Error
    """

    def __init__(self, msg):
        super(FeedsHTTPError, self).__init__(msg, FeedsHTTPError)


class FeedsParseError(FeedsBaseException):
    """
    Exception when Feed could not be parsed.
    """

    def __init__(self, msg):
        super(FeedsParseError, self).__init__(msg, FeedsParseError)


class FeedsSameError(FeedsBaseException):
    """
    Exception when Feed hasn't changed since last time.
    """

    def __init__(self, msg):
        super(FeedsSameError, self).__init__(msg, FeedsSameError)
