#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

import logging

logger = logging.getLogger(__name__)


def feedsocial(object):
    """
    Decorator to perform default sanity checks for all social scoring.
    Also, logging.
    """

    def __init__(self, f):
        self.__f = f

    def __call__(self, *args):
        logger.debug("start: %s", self.__f.__name__)

        logger.debug("end: %s", self.f.__name__)
        return self.__f(*args)
