#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test Management Command
"""

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError


class ManagementTest(TestCase):
    """
    Test Manager Command
    """
    fixtures = [
        "Site.yaml",
        "Feed_all.yaml",
    ]

    def setUp(self):
        """
        Set up environment to test the API
        """
        pass

    def test_refresh(self):
        """
        This calls the 'refresh' Command.

        .. todo:: A real testcase. Right now this test only ensures the code
                  runs with no exception, respectivly the correct exception.
                  However, the command does not return anything.
        """
        call_command("refresh", "1")
        with self.assertRaises(CommandError):
            call_command("refresh", "999")
        self.assertEqual(0, 0)

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass
