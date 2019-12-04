#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""
import logging
import datetime
from django.db import models

from .post import Post


class Rating(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='ratings',
        on_delete=models.CASCADE,
    )

    # Social
    updated = models.DateTimeField(
        auto_now_add=True,
    )

    tweets = models.IntegerField(default=0)
    blogs = models.IntegerField(default=0)
    plus1 = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    linkedin = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    pageviews = models.IntegerField(default=0)

    # NLPM
    sentiment = models.FloatField()

    # all together
    score = models.IntegerField(default=0)

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"

    def __str__(self):
        return "%s (%s)" % (self.post, self.score)
