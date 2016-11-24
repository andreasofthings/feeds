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
        self.f = f

    def __call__(self, *args):
        logger.debug("start: %s", self.f.__name__)

        try:
            from social.get import tweets, facebook, linkedin, plusone
        except:
            logger.error("social not installed")
            return

        if not args.post_id:
            """
            failed
            """
            logger.error("Provided an invalid post_id")
            return
        result = self.f(*args)
        logger.debug("end: %s", self.f.__name__)
        return result
