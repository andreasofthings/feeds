#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
urly.py to allow tests in travis-ci
"""

from django.conf.urls import patterns, url, include, handler404

urlpatterns = patterns('',
    url(r'^feeds/', include( 'feeds.urls', namespace="planet", app_name="planet")),
)


