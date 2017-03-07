#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Announcement Buffer.
=======================

Model acting as a queue to remember which user shared to which channel.

The model keeps the user, the post, the time of scheduling and the time of
execution, along with the channels it is supposed to be sent to.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .options import Options
from .post import Post

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class SocialBuffer(models.Model):
    """
    """

    user = models.ForeignKey(
        Options,
        verbose_name=_('User post'),
        related_name='user_post'
    )
    """Reference to the user that plans to announce the post."""

    post = models.ForeignKey(Post, related_name="post")
    """reference to the post that shall be announced."""

    scheduled = models.DateTimeField(AUTO_ADD_NOW=True)
    executed = models.DateTimeField(Null=True)



    def __str__(self):
        """
        return user and post
        """
        return _(u'%s [for %s]' % (self.post, self.owner))
