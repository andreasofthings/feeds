#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User


class ViewsLoggedInTest(TestCase):
    """
    Test Options views for users that are authenticated.
    """

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(
            self.username,
            'lennon@thebeatles.com',
            self.password
        )
        """Test user."""

    def test_options(self):
        """
        """
        client = Client()
        client.login(username=self.username, password=self.password)
        result = client.get(reverse('planet:options'))
        self.assertEquals(result.status_code, 200)
