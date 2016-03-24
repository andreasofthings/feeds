#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
:mod:`feeds.mixins`

"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class UserAgentRequiredMixin(UserPassesTestMixin):
    user_agent = None  # Default required agent to none

    def test_func(self, user):
        """
            check for useragent
        """

        return 'google' in getattr(
            self.request.META,
            'HTTP_USER_AGENT',
            ''
        ).lower()


class FeedsLevelOneMixin(LoginRequiredMixin):
    pass


class FeedsLevelTwoMixin(FeedsLevelOneMixin, PermissionRequiredMixin):
    permission_required = "feeds.can_backup_feed"
