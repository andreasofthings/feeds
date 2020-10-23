#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from django.contrib.auth import get_user_model

from feeds.views import OptionsView
from feeds.models import Options

import logging

logger = logging.getLogger(__name__)

User = get_user_model()  # instead of importing, get the custom model.


class OptionsViewsTest(TestCase):
    """
    Test Options views for users that are authenticated.
    """

    username = "john"
    realname = "John Lennon"
    password = "password"

    fixtures = [
        # 'socialaccount.socialapp.yaml'
    ]

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(
            self.username,
            self.realname,
            self.password
        )
        self.user.save()
        """Test user."""

    def test_options_anonymous(self):
        """
        Try to view options as anonymous.
        """
        client = Client()
        response = client.get(reverse('planet:options'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/login/?next=%s' % (reverse('planet:options'))
        )

    def test_options_user(self):
        """
        Try to view options as anonymous.
        """
        request = self.factory.get(reverse('planet:options'))
        request.user = self.user
        response = OptionsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_options_post(self):
        """
        Try to view options as anonymous.
        """
        self.test_options_user()
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(
            reverse('planet:options'),
            {
                'number_initially_displayed': "11",
                'max_entries_saved': "101",
                'number_additionally_displayed': "9",
                'submit': "Submit",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertNumQueries(1)

        request = self.factory.get(
            reverse('planet:options'),
            {
                'number_initially_displayed': "11",
            }
        )
        request.user = self.user
        response = OptionsView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertNumQueries(1)

        """
        .. todo:: This should actually be '11', after
        we updated the value above.
        """
        options = Options.objects.get(user=self.user)
        self.assertEqual(options.user, self.user)
        # self.assertEqual(options.number_initially_displayed, 11)
