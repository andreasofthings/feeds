#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase
from django.contrib.auth.models import User


class TestSiteWithCredential(TestCase):
    """
    Test those aspects of :py:mod:`feeds.views` related to
    py:mod:`feeds.models.Site`, that require Credentials.
    """

    username = "john"
    realname = "John Lennon"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(
            self.username,
            self.realname,
            self.password
        )
        """Test user."""

        self.user.user_permissions.add('')
        """Give the test user proper permission."""
