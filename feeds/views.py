#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
:mod:`feeds.views`

Views for :py:mod:`feeds`
=========

The views module contains all Django Class Based Views, marking up the
Frontend to managing and reading :py:mod:`feeds.models.Feed`,
:py:mod:`feeds.models.Post` and :py:mod:`feeds.models.Subscriptions`.

"""

import logging

from datetime import timedelta

from django import forms
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView, RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Options
from .forms import OptionsForm
from .forms import OPMLForm

from .models import WebSite, Feed, Post, Subscription, PostReadCount
from .forms import FeedCreateForm
from .forms import FeedUpdateForm
from .forms import WebSiteCreateForm, WebSiteFeedAddForm, WebSiteUpdateForm
from .tools import getFeedsFromSite
from .baseviews import PaginatedListView

from formtools.wizard.views import SessionWizardView

from el_pagination.views import AjaxListView

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """
    Marketing Page
    ==============

    The HomeView will print out a marketing page, where new users are supposed
    to come to first. It is often referred to as the `landingpage`.

    It does not have any functionality.
    """
    template_name = "feeds/home.html"


class OptionsView(LoginRequiredMixin, UpdateView):
    """
    Options Page
    ============

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
        return reverse('planet:options')

    def get_object(self, queryset=None):
        obj, created = Options.objects.get_or_create(user=self.request.user)
        if created:
            obj.save()
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(OptionsView, self).form_valid(form)


def opmlImport(opml, count=0):
    for node in opml.iter('outline'):
        name = node.attrib.get('text')
        url = node.attrib.get('xmlUrl')
        if name and url:
            logger.debug('  %s :: %s', name, url)
            f, c = Feed.objects.get_or_create(
                feed_url=url,
                name=name,
            )
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
        return reverse("planet:home")

    def form_valid(self, form):
        from xml.etree import ElementTree
        tree = ElementTree.parse(self.request.FILES['opml'])
        opmlImport(tree)
        return super(OPMLView, self).form_valid(form)


WebSiteSubmitForms = [
    ('WebSite', WebSiteCreateForm),
    ('Feeds', WebSiteFeedAddForm),
    ]


class WebSiteSubmitWizardView(SessionWizardView):
    """
    Wizard that walks people through when adding a site with feeds
    """
    template_name = "feeds/website_submit_wizard.html"
    form_list = [WebSiteCreateForm, WebSiteFeedAddForm]

    def get_form(self, step=None, data=None, files=None):
        form = super(WebSiteSubmitWizardView, self).get_form(step, data, files)

        step = step or self.steps.current

        if step == u'Feeds':
            # form = WebSiteFeedAddForm()
            step_0_data = self.storage.get_step_data('WebSite')
            links = getFeedsFromSite(step_0_data['WebSite-url'])
            for title, href in links:
                form.fields[href] = forms.BooleanField(
                    initial=False,
                    required=False,
                    label=title
                )
        return form

    def done(self, form_list, form_dict, **kwargs):
        from django.contrib import messages
        site_form = form_dict['WebSite']
        feed_form = form_dict['Feeds']
        if site_form.is_valid() and feed_form.is_valid():
            site = WebSite(url=site_form.url).save()
            for feed in feed_form.fields:
                f = Feed.get_or_create(
                    website=site,
                    feed_url=feed.url,
                    name=feed.name
                )
                f.save()

            messages.add_message(
                self.request,
                messages.INFO,
                _("Successfully submitted site.")
                )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("Error submitted site.")
            )
        return HttpResponseRedirect(reverse('planet:website-home'))


class WebSiteListView(PaginatedListView):
    """
    Lists all sites in the database.

    The view is accessible publically.

    :url: planet:site-home

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    model = WebSite
    template_name = "feeds/website_list.html"


class WebSiteCreateView(PermissionRequiredMixin, CreateView):
    """
    View to create a new site.
    """
    permission_required = "feeds.add_site"
    form_class = WebSiteCreateForm
    model = WebSite


class WebSiteDetailView(DetailView):
    """
    Shows Details for one particular :py:mod:`feeds.models.WebSite`.

    The view is accessible publically.

    :url: planet:site-detail

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    model = WebSite
    template_name = "feeds/website_detail.html"


class WebSiteUpdateView(PermissionRequiredMixin, UpdateView):
    """
    View to update an existing site.
    """
    permission_required = "feeds.change_site"
    form_class = WebSiteUpdateForm
    model = WebSite


class WebSiteDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "feeds.delete_site"
    model = WebSite
    success_url = "planet:site-home"


class FeedCreateView(PermissionRequiredMixin, CreateView):
    """
    View to create a new feed.

    Required login and credentials.
    """
    permission_required = "feeds.add_feed"
    form_class = FeedCreateForm
    model = Feed
    initial = {'is_Active': False}


class FeedListView(LoginRequiredMixin, PaginatedListView):
    """
    List all registered feeds

    """
    model = Feed
    context_object_name = "feeds"
    queryset = Feed.objects.all()


class FeedDetailView(LoginRequiredMixin, DetailView):
    """
    Show details for a particular feed.

    .. todo:: The view for `Feed Details` shall include stats for the
              particular `Feed`. It is a plain Class Based View right now.
    """
    model = Feed
    queryset = Feed.objects.all()

    def get_context_data(self, **kwargs):
        context = super(FeedDetailView, self).get_context_data(**kwargs)
        context['posts'] = self.object.posts.order_by('-published')
        return context


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a particular feed
    """
    form_class = FeedUpdateForm
    model = Feed

    def get_success_url(self):
        if 'slug' in self.kwargs:
            return reverse('planet:feed-detail', self.kwargs['slug'])
        else:
            return reverse('planet:feed-home')


class FeedDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a particular feed
    """
    model = Feed

    def get_success_url(self):
        return reverse('planet:feed-home')


class FeedRefreshView(LoginRequiredMixin, RedirectView):
    """
    Refresh a particular feed
    """
    permanent = False

    def get_redirect_url(self, pk):
        from feeds.tasks import feed_refresh
        feed_refresh.delay(pk)
        return reverse('planet:feed-detail', args=(pk,))


class FeedSubscribeView(LoginRequiredMixin, RedirectView):
    """
    Subscribe user to a feed
    """
    permanent = False

    def get_redirect_url(self, pk):
        user = Options.objects.get(user=self.request.user)
        feed = Feed.objects.get(pk=pk)
        s, created = Subscription.objects.get_or_create(user=user, feed=feed)
        if created:
            s.save()
        return reverse('planet:feed-detail', args=(pk,))


class FeedUnSubscribeView(LoginRequiredMixin, RedirectView):
    """
    UnSubscribe user to a feed
    """
    permanent = False

    def get_redirect_url(self, pk):
        user = Options.objects.get(user=self.request.user)
        feed = Feed.objects.get(pk=pk)
        s = Subscription.objects.get(user=user, feed=feed)
        s.delete()
        return reverse('planet:feed-detail', args=(pk,))


class FeedSubscriptionsView(LoginRequiredMixin, PaginatedListView):
    """
    List all Feeds one users subscribed to.

    .. reverse-url: 'planet:feed-subscriptions'

    See also:

      - :py:mod:`feeds.views.FeedSubscribeView`
      - :py:mod:`feeds.views.FeedUnsubscribeView`
    """
    model = Feed
    context_object_name = "feeds"
    template_name = "feeds/feed_list.html"

    def get_queryset(self):
        user, created = Options.objects.get_or_create(user=self.request.user)
        if created:
            user.save()
        queryset = Feed.objects.filter(feed_subscription__user=user)
        return queryset


class PostListView(AjaxListView):
    """
    List Posts from all Feeds.

    .. todo: Pagination does not work properly. Some sort of limit would be
    nice, too. The pagination bar looks really ugly.
    """
    model = Post
    # paginate_by = 50

    def get_queryset(self):
        """
        Apparently some feeds give posts that only have a timestamp 'published'
        from the future. We prevent displaying these by filtering for older
        than today/now.

        :py:module:`PostManager.older_than` provides this functionality and
        exposes it as the :py:module:`Post.objects` Manager.
        """
        return Post.objects.older_than(timedelta(0)).order_by('-published')


class PostSubscriptionView(LoginRequiredMixin, AjaxListView):
    """
    List Posts from subscribed Feeds.

    .. todo:: At the time being `PostSubscriptionView` is a bare stub.
              It does not yet have the correct `queryset`, that limits
              results to posts from actually subscribed feeds, neither
              does it have a proper tests for the functionality.

              Also, this view is not accessiable through an URL for now.

    .. reverse-url: 'planet:post-subscription-home'
    """
    model = Post
    paginate_by = 50

    def get_queryset(self):
        user = Options.objects.get(user=self.request.user)
        user_subscriptions = Subscription.objects.feeds(user)
        subscriptions = Post.objects.filter(feed_id__in=user_subscriptions)
        return subscriptions.order_by('-published')


class PostDetailView(DetailView):
    """
    View a post and related metadata.

    Requires login and permissions.
    """
    user_agent = "google"
    model = Post
    permissions = {
        "any": ("feeds.delete_post", "feeds.change_post", "feeds.add_post",)
    }


class PostTrackableView(RedirectView):

    permanent = False

    def get_redirect_url(self, pk):
        post = get_object_or_404(Post, pk=pk)
        PostReadCount(post=post).save()
        """Increase Read Counter for this post."""
        return post.link
        """And return to the actual link."""
