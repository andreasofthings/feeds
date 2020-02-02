#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Object Serializers.
===================

help serializing.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from rest_framework import serializers
from .models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta."""
        model = Feed
