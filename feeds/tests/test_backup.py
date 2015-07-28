#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse


class BackupTest(TestCase):
    """
    Test whether all :py:mod:`feeds.views` are working.

    .. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'Feed_all.yaml',
        'Categories.yaml',
    ]

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up environment.
        """

        self.client = Client()
        """Test Client."""

        self.user = User.objects.create_user(
            self.username,
            'lennon@thebeatles.com',
            self.password
        )
        """Test user."""
        permission = Permission.objects.get(codename="backup_feed")
        self.user.user_permissions.add(permission)

    def test_backup(self):
        """
        """
        result = self.client.get(reverse('planet:backup'))
        self.assertEqual(result.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        result = self.client.get(reverse('planet:backup'))
        self.assertEqual(result.status_code, 200)
