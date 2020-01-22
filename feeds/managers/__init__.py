#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Managers
========
"""

from django.db import models
from .category import CategoryManager
from .editorcategory import EditorCategoryManager
from .feed import FeedManager
from .post import PostManager
from .subscription import SubscriptionManager
from .tag import TagManager
from .option import OptionsManager
from .website import WebSiteManager

__all__ = [
    'CategoryManager',
    'EditorCategoryManager',
    'FeedManager',
    'OptionsManager',
    'PostManager',
    'PostReadCountManager',
    'SubscriptionManager',
    'TagManager',
    'WebSiteManager',
]


class PostReadCountManager(models.Manager):
    """
    Manager for PostReadCount objects
    """
    pass
