#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Managers
========
"""

from django.db import models


class WebSiteManager(models.Manager):
    """
    :py:mod:`WebSiteManager` provide extra functions.
    """
    def __init__(self, *args, **kwargs):
        return super(WebSiteManager, self).__init__(*args, **kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class TagManager(models.Manager):
    """
    Manager for `Tag` objects.
    """

    def get_by_natural_key(self, name):
        """
        get Tag by natural key, to allow serialization by key rather than `ìd`
        """
        return self.get(name=name)


class CategoryManager(models.Manager):
    """
    Manager for Category
    """
    def get_by_natural_key(self, name):
        """
        Get Category by natural kea to allow serialization
        """
        return self.get(name=name)


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


class PostReadCountManager(models.Manager):
    """
    Manager for PostReadCount objects
    """
    pass

class OptionsManager(models.Manager):
    def get(self, *args, **kwargs):
        """
        Override get to ensure Options are created if not existing yet.
        """
        obj, created = self.get_or_create(*args, **kwargs)
        if created:
            obj.save()
        return super(OptionsManager, self).get(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        return super(OptionsManager, self).__init__(*args, **kwargs)
