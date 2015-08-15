#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
:mod:`feeds.mixins`

"""

from django.conf import settings
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import AnonymousUser

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import UserPassesTestMixin


def google_required(func):
    """
    find googlebot in useragent

    require other users to login
    """
    def _view(request, *args, **kwargs):
        if 'HTTP_USER_AGENT' in request.META:
            useragent = request.META['HTTP_USER_AGENT']
            params = request.META.get('QUERY_STRING', "")
            if request.user.is_anonymous() and \
                    "googlebot" not in useragent.lower() and \
                    "login" not in params:
                return HttpResponseRedirect(settings.LOGIN_URL)
            else:
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return _view


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
            return int(getattr('paginate_by', self.request.GET, 10))
        # elif type(self.request.user) is not AnonymousUser:
        #    if 'number_initially_displayed' in self.request.user.options:
        #        return self.request.user.options.number_initially_displayed
        return 10


class FeedsLevelOneMixin(LoginRequiredMixin):
    pass


class FeedsLevelTwoMixin(FeedsLevelOneMixin, PermissionRequiredMixin):
    permission_required = "feeds.can_backup_feed"
