#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
:mod:`feeds.mixins`

"""

def google_required(func):
    """
    find googlebot in useragent

    require other users to login
    """
    def _view(request, *args, **kwargs):
        if request.META.has_key('HTTP_USER_AGENT'):
            useragent = request.META['HTTP_USER_AGENT']
            if request.user.is_anonymous() and not "googlebot" in useragent.lower():
                return HttpResponseRedirect(reverse("userprofile:login"))
            else:
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("userprofile:login"))
    return _view

class LoginRequiredMixin(object):
    """
    Generic Mixin that dispatches login_required to Generic Views
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class PermissionRequiredMixin(object):
    """
    Example:
    class View(PermissionRequiredMixin, ListView):
    ...
    require_permissions = (
        'app.permission',
        ...
    )
    ...
    """
    require_permissions = ()
     
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.require_permissions):
            messages.error(
                request,
                _('You do not have the permission required to perform the requested view.')
            )
            return HttpResponseRedirect(reverse('userprofile:login'))
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

# vim: ts=4 et sw=4 sts=4

