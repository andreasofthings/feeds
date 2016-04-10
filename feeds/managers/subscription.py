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
        Return feeds subscribed by user.

        .. todo: Implement this.
        """
        return self.objects.filter(user=user).feed.all()
