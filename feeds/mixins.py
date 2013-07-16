#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
:mod:`feeds.mixins`

"""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.views import redirect_to_login
from braces.views import AccessMixin

def google_required(func):
    """
    find googlebot in useragent

    require other users to login
    """
    def _view(request, *args, **kwargs):
        if request.META.has_key('HTTP_USER_AGENT'):
            useragent = request.META['HTTP_USER_AGENT']
            if request.user.is_anonymous() and not "googlebot" in useragent.lower():
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
            Check to see if the request's user has the required permission.
            """
            if request.META.has_key('HTTP_USER_AGENT'):
               agent = request.META['HTTP_USER_AGENT']
            else:
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied
                else:
                    return redirect_to_login(request.get_full_path(),
                                             self.get_login_url(),
                                             self.get_redirect_field_name())

            if not self.user_agent in agent:
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied
                else:
                    return redirect_to_login(request.get_full_path(),
                                            self.get_login_url(),
                                            self.get_redirect_field_name())

            return super(UserAgentRequiredMixin, self).dispatch(request,
                *args, **kwargs)


# vim: ts=4 et sw=4 sts=4

