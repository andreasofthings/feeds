"""
:mod:`feeds.views.views`.

Views for :py:mod:`feeds`
=========

The views module contains all Django Class Based Views, marking up the
Frontend to managing and reading :py:mod:`feeds.models.Feed`,
:py:mod:`feeds.models.Post` and :py:mod:`feeds.models.Subscriptions`.

"""
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4


import logging


from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView, RedirectView

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _

from ..forms import OptionsForm
from ..forms import OPMLForm

from ..models import Feed, Subscription, Options
from ..forms import FeedCreateForm
from ..forms import FeedUpdateForm
from ..mixins import PaginateListMixin

# from ..baseviews import PaginatedListView


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """
    Marketing Page.

    The HomeView will print out a marketing page, where new users are supposed
    to come to first. It is often referred to as the `landingpage`.

    It does not have any functionality.
    """

    template_name = "feeds/home.html"


class OptionsView(LoginRequiredMixin, UpdateView):
    """
    Options Page.

    The `OptionsView` will allow individual users to manage settings/options
    related to their account and viewing experience.

    Options managed here are kept in :py:mod:`feeds.models.Options`
    The form to display them is kept in :py:mod:`feeds.forms.OptionsForm`

    .. todo:: The entire `options` approach should be architected better
              and have better tests. Contained options are neither complete
              nor are these consequently used across the codebase.

    .. codeauthor:: Andreas Neumeier
    """

    model = Options
    template_name = "feeds/options.html"
    form_class = OptionsForm

    def get_success_url(self):
        """Get success url."""
        return reverse("planet:options")

    def get_object(self, queryset=None):
        """Get object."""
        obj, created = Options.objects.get_or_create(user=self.request.user)
        if created:
            obj.save()
        return obj

    def form_valid(self, form):
        """Validate Form."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(OptionsView, self).form_valid(form)


def opmlImport(opml, count=0):
    for node in opml.iter("outline"):
        name = node.attrib.get("text")
        url = node.attrib.get("xmlUrl")
        if name and url:
            logger.debug("  %s :: %s", name, url)
            f, c = Feed.objects.get_or_create(feed_url=url, name=name)
            if c:
                f.save()
    return True


class OPMLView(FormView):
    """
    View to allow import of OPML Files.

    .. todo:: The `OPML Import` should work on a per user basis.
              OPML is plain text format, but since uploaded by individuals,
              that should reflect in user/ownership.
    """

    form_class = OPMLForm
    template_name = "feeds/opml.html"

    def get_success_url(self):
        """Get success url."""
        return reverse("planet:home")

    def form_valid(self, form):
        """Form Valid."""
        from xml.etree import ElementTree

        tree = ElementTree.parse(self.request.FILES["opml"])
        opmlImport(tree)
        return super(OPMLView, self).form_valid(form)


class FeedCreateView(PermissionRequiredMixin, AccessMixin, CreateView):
    """
    Create a new feed.

    Required login and credentials.
    """

    permission_required = "feeds.add_feed"

    def get_permission_denied_message(self):
        """Get permission_denied message."""
        from django.contrib import messages
        messages.add_message(
            self.request,
            messages.INFO,
            _("You don't have the permission to add new Feeds.")
        )
        return "You cannot add new Feeds."

    raise_exception = False
    form_class = FeedCreateForm
    model = Feed
    initial = {"is_Active": False}


class FeedListView(LoginRequiredMixin, PaginateListMixin, ListView):
    """List all registered feeds."""

    model = Feed
    queryset = Feed.objects.order_by("name")


class FeedDetailView(LoginRequiredMixin, DetailView):
    """
    Show details for a particular feed.

    .. todo:: The view for `Feed Details` shall include stats for the
              particular `Feed`. It is a plain Class Based View right now.
    """

    model = Feed
    queryset = Feed.objects.all()

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super(FeedDetailView, self).get_context_data(**kwargs)
        context["posts"] = self.object.posts.order_by("-published")
        return context


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    """Update a particular feed."""

    form_class = FeedUpdateForm
    model = Feed

    def get_success_url(self):
        """Get success url."""
        return reverse("planet:feed-detail", args=(self.kwargs["pk"],))


class FeedDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a particular feed."""

    model = Feed

    def get_success_url(self):
        """Get success url."""
        return reverse("planet:feed-home")


class FeedRefreshView(LoginRequiredMixin, RedirectView):
    """Refresh a particular feed."""

    permanent = False

    def get_redirect_url(self, pk):
        """Refresh Feed and return redirect url."""
        f = Feed.objects.get(pk=pk)
        f.refresh()
        return reverse("planet:feed-detail", args=(pk,))


class FeedSubscribeView(LoginRequiredMixin, RedirectView):
    """Subscribe user to a feed."""

    permanent = False

    def get_redirect_url(self, pk):
        """Subscribe User and redirect."""
        user = Options.objects.get(user=self.request.user)
        feed = Feed.objects.get(pk=pk)
        s, created = Subscription.objects.get_or_create(user=user, feed=feed)
        if created:
            s.save()
        return reverse("planet:feed-detail", args=(pk,))


class FeedUnSubscribeView(LoginRequiredMixin, RedirectView):
    """UnSubscribe user to a feed."""

    permanent = False

    def get_redirect_url(self, pk):
        """Unsubscribe User and redirect."""
        user = Options.objects.get(user=self.request.user)
        feed = Feed.objects.get(pk=pk)
        s = Subscription.objects.get(user=user, feed=feed)
        s.delete()
        return reverse("planet:feed-detail", args=(pk,))


class FeedSubscriptionsView(LoginRequiredMixin, PaginateListMixin, ListView):
    """
    List all Feeds one user subscribed.

    .. reverse-url: 'planet:feed-subscriptions'

    See also:
      - :py:mod:`feeds.views.FeedSubscribeView`
      - :py:mod:`feeds.views.FeedUnsubscribeView`

    """

    model = Feed
    context_object_name = "feeds"
    template_name = "feeds/feed_list.html"

    def get_queryset(self):
        """
        Return Queryset.

        Custom Queryset.
        """
        user, created = Options.objects.get_or_create(user=self.request.user)
        if created:
            user.save()
        queryset = Feed.objects.filter(feed_subscription__user=user)
        return queryset.order_by("name")
