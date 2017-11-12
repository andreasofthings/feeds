#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""
import logging
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from .post import Post

class Rating(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='ratings',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    # Social
    updated_social = models.DateTimeField(null=True, blank=True, default=False)

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

    def __str__(self):
        return "%s (%s)" % (self.post, self.score)
