#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
:mod:`feeds.views`

views for feeds

"""

import logging

from django import forms
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView, ListView
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView, RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from .models import Options
from .forms import OptionsForm
from .forms import OPMLForm

from .models import Site, Feed, Post, Subscription
from .models import Category, Tag, PostReadCount
from .forms import FeedCreateForm, CategoryCreateForm, TagCreateForm
from .forms import FeedUpdateForm, CategoryUpdateForm
from .forms import SiteCreateForm, SiteFeedAddForm, SiteUpdateForm

from formtools.wizard.views import SessionWizardView

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """
    Marketing Page

    This is where new users are supposed to come to first.
    """
    template_name = "feeds/home.html"


class OptionsView(LoginRequiredMixin, UpdateView):
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


def opml_import(opml, count=0):
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
                try:
                    f.save()
                except Exception as e:
                    logger.debug(e)
        else:
            logger.debug("Category: %s", name)
    return True


class OPMLView(FormView):
    """
    View to allow import of OPML Files.

    .. todo:: This should be per user. OPML allows user/ownership.
    """
    form_class = OPMLForm
    template_name = "feeds/opml.html"
    success_url = "planet:home"

    def form_valid(self, form):
        from xml.etree import ElementTree
        tree = ElementTree.parse(self.request.FILES['opml'])
        opml_import(tree)
        return super(OPMLView, self).form_valid(form)


SiteSubmitForms = [
    ('Site', SiteCreateForm),
    ('Feeds', SiteFeedAddForm),
    ]


class SiteSubmitWizardView(SessionWizardView):
    """
    Wizard that walks people through when adding a site with feeds
    """
    template_name = "feeds/site_submit_wizard.html"
    form_list = [SiteCreateForm, SiteFeedAddForm]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')

    def get_form(self, step=None, data=None, files=None):
        form = super(SiteSubmitWizardView, self).get_form(step, data, files)

        step = step or self.steps.current

        if step == u'Feeds':
            step_0_data = self.storage.get_step_data('Site')
            form = SiteFeedAddForm()
            html = requests.get(step_0_data['Site-url'])
            soup = BeautifulSoup(html.text)
            for link in soup.head.find_all('link'):
                if 'type' in link:
                    if "application/rss" in link.get('type'):
                        form.fields[link.get('href')] = forms.BooleanField(
                            initial=False,
                            required=False,
                            label=link.get('title')
                        )

        return form


class SiteListView(ListView):
    """
    Lists all sites in the database.

    The view is accessible publically.

    :url: planet:site-home

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    model = Site
    template_name = "feeds/site_list.html"


class SiteCreateView(PermissionRequiredMixin, CreateView):
    """
    View to create a new site.
    """
    permission_required = "feeds.add_site"
    form_class = SiteCreateForm
    model = Site


class SiteDetailView(DetailView):
    """
    Shows Details for one particular :py:mod:`feeds.models.Site`.

    The view is accessible publically.

    :url: planet:site-view

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    model = Site
    template_name = "feeds/site_detail.html"


class SiteUpdateView(PermissionRequiredMixin, UpdateView):
    """
    View to update an existing site.
    """
    permission_required = "feeds.change_site"
    form_class = SiteUpdateForm
    model = Site


class SiteDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "feeds.delete_site"
    model = Site
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


class FeedListView(ListView):
    """
    List all registered feeds

    """
    model = Feed
    context_object_name = "feeds"
    queryset = Feed.objects.all()

    def get_paginate_by(self, queryset):
        return 10


class FeedDetailView(DetailView):
    """
    Show details for a particular feed.

    ToDo:
    this shall include stats
    """
    model = Feed
    context_object_name = "feed"

    def get_context_data(self, *args, **kwargs):
        context = super(FeedDetailView, self).get_context_data(**kwargs)
        return context


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a particular feed
    """
    form_class = FeedUpdateForm
    model = Feed

    def get_success_url(self):
        if 'slug' in self.kwargs:
            return reverse('planet:feed-view', self.kwargs['slug'])
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
        return reverse('planet:feed-view', args=(pk,))


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
        return reverse('planet:feed-view', args=(pk,))


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
        return reverse('planet:feed-view', args=(pk,))


class FeedSubscriptionsView(LoginRequiredMixin, ListView):
    """
    One users subscriptions
    """
    model = Feed
    context_object_name = "feeds"
    template_name = "feeds/feed_list.html"

    def get_queryset(self):
        user = Options.objects.get(user=self.request.user)
        queryset = Feed.objects.filter(feed_subscription__user=user)
        return queryset


class PostListView(ListView):
    """
    List Posts
    """
    model = Post
    paginate_by = 10
    context_object_name = "nodes"
    queryset = Post.objects.order_by('published')


class PostDetailView(DetailView):
    user_agent = "google"
    permissions = {
        "any": ("feeds.delete_post", "feeds.change_post", "feeds.add_post",)
    }
    model = Post
    context_object_name = "node"

    def dispatch(self, *args, **kwargs):
        return super(PostDetailView, self).dispatch(*args, **kwargs)


class PostTrackableView(RedirectView):

    permanent = False

    def get_redirect_url(self, pk):
        post = get_object_or_404(Post, pk=pk)
        PostReadCount(post=post).save()
        return post.link


class CategoryListView(ListView):
    """
    List all registered feeds

    """
    model = Category
    context_object_name = "categories"
    paginate_by = 10
    # queryset = Category.objects.all()


class CategoryDetailView(DetailView):
    """
    Show details for a particular Category

    ToDo:
    this shall include stats
    """
    model = Category

    def dispatch(self, *args, **kwargs):
        return super(CategoryDetailView, self).dispatch(*args, **kwargs)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a particular Category
    """
    form_class = CategoryUpdateForm
    model = Category

    def get_success_url(self):
        if 'slug' in self.kwargs:
            return reverse('planet:category-view', self.kwargs['slug'])
        else:
            return reverse('planet:category-home')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    ToDo:
    make this more nice & userfriendly
    """
    form_class = CategoryCreateForm
    model = Category
    initial = {'is_Active': False}


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "feeds.delete_category"
    model = Category
    success_url = "planet:category-home"


class TagListView(ListView):
    """
    List all registered tags

    """
    model = Tag
    context_object_name = "tags"
    paginate_by = 10
    queryset = Tag.objects.all()


class TagDetailView(DetailView):
    """
    Show details for a particular tag.

    ToDo:
    this shall include stats
    """
    model = Tag
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        return super(TagDetailView, self).dispatch(*args, **kwargs)


class TagCreateView(LoginRequiredMixin, CreateView):
    """
    ToDo:
    make this more nice & userfriendly
    """
    form_class = TagCreateForm
    model = Tag
    initial = {'is_Active': False}


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Update particular tag
    """
    permission_required = "feeds.update_tag"
    model = Tag
