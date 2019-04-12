#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Aggregator models.
=======================

Stores as much as possible coming out of the feed.
For working with user models:
    - https://wsvincent.com/django-referencing-the-user-model/
.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model

from ..managers import OptionsManager
from .feed import Feed

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Options(models.Model):
    user = models.ForeignKey(
        get_user_model(),  # settings.AUTH_USER_MODEL,
        help_text=_("User"),
        on_delete=models.CASCADE,
    )
    number_initially_displayed = models.IntegerField(
        default=10,
        help_text=_('Paginate by')
    )
    number_additionally_displayed = models.IntegerField(
        default=5,
        help_text=_('ToDo')
    )
    max_entries_saved = models.IntegerField(default=100)

    objects = OptionsManager()

    subscriptions = models.ManyToManyField(Feed, through='Subscription')

    class Meta:
        app_label = "feeds"
        verbose_name_plural = "options"

    def __str__(self):
        return u'%s Options' % self.user
