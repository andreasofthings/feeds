#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Managers
========
"""

from django.db import models


class FeedManager(models.Manager):
    """
    Manager object for :py:mod:`feeds.models.Feed`
    """
    def get_by_natural_key(self, name):
        """
        Get Feed by natural key, to allow
        serialization by key rather than `id`.
        """
        return self.get(name=name)
