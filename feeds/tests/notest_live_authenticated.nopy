#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver


class ClassTestAllViewsAnonymousLive(LiveServerTestCase):
    """
    Test options with browser.
    """
    username = "john"
    realname = "John Lennon"
    password = "password"

    @classmethod
    def setUpClass(cls):
        super(ClassTestAllViewsAnonymousLive, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.user = User.objects.create_superuser(
            cls.username,
            cls.realname,
            cls.password
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ClassTestAllViewsAnonymousLive, cls).tearDownClass()

    def test_home(self):
        """
        Test the home page from browser.
        """
        self.selenium.get(self.live_server_url + reverse('planet:home'))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Feeds', body.text)

    def test_options(self):
        """
        Test the options page from browser.

        .. todo:: This currently only tests for a superuser.
        Also create a regular user.
        """
        self.selenium.get(self.live_server_url + '/admin')

        # She sees the familiar 'Django administration' heading
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('admin', body.text)

        # She types in her username and passwords and
        # hits return
        # username_field = self.browser.find_element_by_name('username')
        # username_field.send_keys(self.username)

        # password_field = self.browser.find_element_by_name('password')
        # password_field.send_keys(self.password)
        # password_field.send_keys(Keys.RETURN)
