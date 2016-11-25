#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium.webdriver.firefox.webdriver import WebDriver


class TestAllViewsAnonymousLive(LiveServerTestCase):
    """
    Test options with browser.
    """
    username = "john"
    realname = "John Lennon"
    password = "password"

    @classmethod
    def setUpClass(cls):
        super(TestAllViewsAnonymousLive, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestAllViewsAnonymousLive, cls).tearDownClass()

    def test_anonymous(self):
        """
        Test the home page from browser.
        """
        self.selenium.get(self.live_server_url + reverse('planet:home'))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Feeds', body.text)

        self.selenium.get(self.live_server_url + reverse('planet:website-home'))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

        self.selenium.get(self.live_server_url + reverse('planet:feed-home'))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

        self.browser.get(self.live_server_url + reverse('planet:post-home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

    def tearDown(self):
        self.browser.quit()
