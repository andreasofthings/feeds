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


class PaginationMixin(object):
    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            return int(getattr(self.request.GET, 'paginate_by', 10))
        # elif type(self.request.user) is not AnonymousUser:
        #    if 'number_initially_displayed' in self.request.user.options:
        #        return self.request.user.options.number_initially_displayed
        return 10


class FeedsLevelOneMixin(LoginRequiredMixin):
    pass


class FeedsLevelTwoMixin(FeedsLevelOneMixin, PermissionRequiredMixin):
    permission_required = "feeds.can_backup_feed"
