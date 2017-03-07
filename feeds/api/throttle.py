#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
.. testsetup:: *

Throttle Classes for API.
"""

from rest_framework.throttling import UserRateThrottle


class WebSiteThrottle(UserRateThrottle):
    rate = "1/second"


class FeedThrottle(UserRateThrottle):
    rate = "1/second"


class PostThrottle(UserRateThrottle):
    rate = "4/second"


class SubscriptionThrottle(UserRateThrottle):
    rate = '1/second'
