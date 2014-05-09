#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from feeds.models import Feed


class TestRSS(TestCase):

    fixtures = ["Feed.yaml", ]

    def test_rss(self):
        c = Client()
        f = Feed.objects.all()[0].pk
        r = c.get(reverse('planet:rss', kwargs={'pk':f,}))
        self.assertEquals(r.status_code, 200)
