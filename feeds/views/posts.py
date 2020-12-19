"""
:mod:`feeds.views.posts`.

Views for :py:mod:`posts`
=========

The views module contains all Django Class Based Views, marking up the
Frontend to reading :py:mod:`feeds.models.Post`.
"""
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4


from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    RedirectView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.dates import (
    ArchiveIndexView, YearArchiveView,
    MonthArchiveView, WeekArchiveView, DayArchiveView
    )

from ..mixins import PaginateListMixin
from ..models import (
    Post, PostReadCount, Subscription, Options
)


class PostListView(PaginateListMixin, LoginRequiredMixin, ListView):
    """
    List Posts from all Feeds.

    .. todo: Pagination does not work properly. Some sort of limit would be
    nice, too. The pagination bar looks really ugly.
    """

    model = Post
    paginate_by = 50

    def get_queryset(self):
        """
        Return Queryset.

        Apparently some feeds give posts that only have a timestamp 'published'
        from the future. We prevent displaying these by filtering for older
        than today/now.

        :py:module:`PostManager.older_than` provides this functionality and
        exposes it as the :py:module:`Post.objects` Manager.

        .. todo::
          Is this redundant?
        """
        return Post.objects.older_than(timedelta(0)).order_by("-published")


class PostTodayView(PaginateListMixin, LoginRequiredMixin, ListView):
    """
    List Posts from all Feeds.

    .. todo: Pagination does not work properly. Some sort of limit would be
    nice, too. The pagination bar looks really ugly.
    """

    model = Post
    queryset = Post.objects.today()
    paginate_by = 50


class PostSubscriptionView(PaginateListMixin, LoginRequiredMixin, ListView):
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
        """
        Return Queryset.

        return custom queryset.
        """
        user = Options.objects.get(user=self.request.user)
        user_subscriptions = Subscription.objects.feeds(user)
        subscriptions = Post.objects.filter(feed_id__in=user_subscriptions)
        return subscriptions.order_by("-published")


class PostDetailView(DetailView):
    """
    View a post and related metadata.

    Requires login and permissions.
    """

    user_agent = "google"
    model = Post
    permissions = {
        "any": (
            "feeds.delete_post",
            "feeds.change_post",
            "feeds.add_post")
        }


class PostTrackableView(RedirectView):
    """
    PostTrackableView.

    Create a trackable view for a `post` through
    redirecting to the actual post.
    """

    permanent = False

    def get_redirect_url(self, pk):
        """Overwrite get_redirect_url."""
        post = get_object_or_404(Post, pk=pk)
        PostReadCount(post=post).save()
        """Increase Read Counter for this post."""
        return post.link
        """And return to the actual link."""


class PostIndexView(ArchiveIndexView):
    """
    Post Archive.

    Based off a Django Generic Date View.
    """

    model = Post
    date_field = "published"


class PostYearArchiveView(YearArchiveView):
    """
    Yearly Post Archive.

    Based off a Django Generic Date View.
    """

    model = Post
    date_field = "published"


class PostMonthArchiveView(MonthArchiveView):
    """
    Monthly Post Archive.

    Based off a Django Generic Date View.
    """

    model = Post
    date_field = "published"
    month_format = '%m'


class PostWeekArchiveView(WeekArchiveView):
    """
    Weekly Post Archive.

    Based off a Django Generic Date View.
    """

    model = Post
    date_field = "published"
    week_format = "%W"


class PostDayArchiveView(DayArchiveView):
    """
    Daily Post Archive.

    Based off a Django Generic Date View.
    """

    model = Post
    date_field = "published"
    month_format = '%m'
