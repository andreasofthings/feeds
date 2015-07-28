#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
:mod:`feeds.mixins`

"""

from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from braces.views import AccessMixin

from django.exceptions import ImproperlyConfigured, PermissionDenied

from braces.views import LoginRequiredMixin, PermissionRequiredMixin


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


class UserAgentRequiredMixin(AccessMixin):
    user_agent = None  # Default required agent to none

    def dispatch(self, request, *args, **kwargs):
        """
        check user authentication
        if not authenticated
            check for useragent
        """

        if self.user_agent is None:
            raise ImproperlyConfigured("'UserAgentRequiredMixin' requires "
                                       "'user_agent' attribute to be set.")

        if not request.user.is_authenticated():
            """
            Check to see if the request's user ha$s the required permission.
            """
            if 'HTTP_USER_AGENT' in request.META:
                agent = request.META['HTTP_USER_AGENT']
            else:
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied
                else:
                    return redirect_to_login(request.get_full_path(),
                                             self.get_login_url(),
                                             self.get_redirect_field_name())

            if self.user_agent not in agent:
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied
                else:
                    return redirect_to_login(request.get_full_path(),
                                             self.get_login_url(),
                                             self.get_redirect_field_name())

            return super(UserAgentRequiredMixin, self).dispatch(
                request,
                *args,
                **kwargs
            )


class FeedsLevelOneMixin(LoginRequiredMixin):
    pass


class FeedsLevelTwoMixin(PermissionRequiredMixin, FeedsLevelOneMixin):
    permission_required = "feeds.add_site"
