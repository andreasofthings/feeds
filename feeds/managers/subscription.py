#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
SubscriptionManager
===================
"""

from django.db import models


class SubscriptionManager(models.Manager):
    """
    """
    def feeds(self, user):
        """
        Returns a list of feed-ids the user subscribed to.

        .. todo: Careful, it's IDs!, not instances returned.
        """
        return self.filter(user=user).values_list('feed', flat=True)
