#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Aggregator models.
=======================

Stores as much as possible coming out of the feed.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .options import Options
from .feed import Feed
from ..managers import SubscriptionManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Subscription(models.Model):
    """
    User Feed Subscription
    """
    user = models.ForeignKey(
        Options,
        verbose_name=_('User Subscription'),
        related_name='user_subscription'
    )
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('Feed Subscription'),
        related_name='feed_subscription'
    )

    objects = SubscriptionManager()

    class Meta:
        unique_together = (("user", "feed"),)

    def __str__(self):
        return u'%s subscribed [%s]' % (self.user, self.feed)
