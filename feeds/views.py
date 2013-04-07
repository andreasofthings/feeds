#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
:mod:`feeds.views`

views for feedbrater

"""

import simplejson as json
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView, RedirectView
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc

from feeds.models import Feed, Post, Category, Tag, PostReadCount
from feeds.forms import FeedCreateForm, CategoryCreateForm, TagCreateForm
from feeds.forms import FeedUpdateForm, CategoryUpdateForm

from feeds.mixins import LoginRequiredMixin, PermissionRequiredMixin, google_required

class BraterView(TemplateView):
    template_name = "feeds/brater.html"

class FeedCreateView(PermissionRequiredMixin, CreateView):
    """
    View to create a new feed.

    Required login and credentials.
    """
    require_permissions = (
        'feeds.add_feed',
    )
    form_class = FeedCreateForm
    model = Feed
    initial = {'is_Active': False}

class FeedListView(ListView):
    """
    List all registered feeds

    """
    model = Feed
    context_object_name = "feeds"
    queryset = Feed.objects.filter(beta=True)

    def get_paginate_by(self, queryset):
        return 10

class FeedDetailView(DetailView):
    """
    Show details for a particular feed.

    ToDo:
    this shall include stats
    """
    model = Feed

    def get_context_data(self, *args, **kwargs):
        context = super(FeedDetailView, self).get_context_data(**kwargs)
        clickdata = []
        contentdata = []
        labels = []
        now = datetime.utcnow().replace(tzinfo=utc)

        clicklist = PostReadCount.objects.filter(post__feed__id=self.kwargs['pk'])
        import random
        for i in range(24):
            upper_offset = now - timedelta(hours=i)
            lower_offset = now - timedelta(hours=i+1)
            if clicklist:
                clickdata.append(clicklist.filter(created__gte=lower_offset).filter(created__lte=upper_offset).count())
            else:
                clickdata.append(0)
            contentdata.append(random.Random().randint(0,7))
            labels.append("%s:00"%(str(lower_offset.hour)))

        chartdata = {
            'labels': labels,
            'datasets': [ {
                  'fillColor' : "rgba(220,220,220,0.5)",
                  'strokeColor' : "rgba(220,220,220,1)",
                  'pointColor' : "rgba(220,220,220,1)",
                  'pointStrokeColor' : "#fff",
                  'data': contentdata,
            }, {
                  'fillColor' : "rgba(200,200,250,0.5)",
                  'strokeColor' : "rgba(220,220,220,1)",
                  'pointColor' : "rgba(220,220,220,1)",
                  'pointStrokeColor' : "#fff",
                  'data': clickdata,
            },
            ]
        }
        context['data'] = json.dumps(chartdata)

        context['top5'] = Post.objects.filter(feed__id=self.kwargs['pk'])[:5]
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
        feed_refresh.delay(feed_id=pk)
        return reverse('planet:feed-view', args=(pk,))

class PostListView(ListView):
    """
    List Posts
    """
    model = Post
    paginate_by = 10
    context_object_name = "nodes"
    object_list = "nodes"
    queryset = Post.objects.order_by('-published')

class PostDetailView(DetailView):
    model = Post
    context_object_name = "node"

    @method_decorator(google_required)
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

# vim: ts=4 et sw=4 sts=4

