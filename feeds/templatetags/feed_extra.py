#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

from django import template
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, Group

from ..models import Feed, Post, Subscription, Options

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return True if group in user.groups.all() else False


class RecentPostNode(template.Node):
    """
    TemplateTag RenderNode

    renders recent posts for a feed.(pk)
    """
    def __init__(self, feed, var_name):
        self.feed = template.Variable(feed)
        self.var_name = var_name
        self.max_posts = 5

    def render(self, context):
        try:
            feed = self.feed.resolve(context)
        except Feed.MultipleObjectsReturned:
            raise template.TemplateSyntaxError(
                """
                'recent_posts' template tag requires 'feed' as first argument.
                Got this instead:
                %r (type: %r)
                """ %
                self.feed, type(self.feed)
            )
        try:
            recent = Post.objects.latest().filter(
                feed=feed
            )[:self.max_posts]
        except Post.DoesNotExist:
            recent = Post.objects.none()
        context[self.var_name] = recent
        return ''


@register.tag('recent_posts')
def recent_posts(parser, token):
    """
    recent_posts
    ============

    Templatetag to render recent posts for a feed.
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" %
            token.contents.split()[0]
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    feed, var_name = m.groups()
    return RecentPostNode(feed, var_name)


class FeedControlsNode(template.Node):
    """
    TemplateTag RenderNode

    renders controls for a feed object.
    """

    button = """
    <a href="%s" class="btn btn-sm" role="button"
    data-toggle="tooltip" data-placement="top" title="%s">
    <span class="fas fa-%s"></span>
    </a>
    """

    def __init__(self, feed):
        self.feed = template.Variable(feed)

    def render(self, context):
        try:
            feed = self.feed.resolve(context)
        except Feed.MultipleObjectsReturned:
            raise template.TemplateSyntaxError(
                """
                'feed_controls' template tag
                requires 'feed' as first argument.
                Got this instead: \n
                %r (type: %r)
                """ %
                self.feed, type(self.feed)
            )

        """
        Before Django 1.10 / Feeds 2016.09.30:
        user = template.resolve_variable('user', context)

        The function has been informally marked as “Deprecated” for some time.
        Replace resolve_variable(path, context) with
        django.template.Variable(path).resolve(context).

        Hence:
        """
        user = template.Variable('user').resolve(context)

        absolute_url = feed.get_absolute_url()

        view_button = self.button % (
            absolute_url,
            _('View Feed'),
            'search'
        )
        subscribe_button = self.button % (
            reverse('planet:feed-subscribe', kwargs={'pk': feed.pk}),
            _('Subscribe to Feed'),
            'check-circle'
        )
        unsubscribe_button = self.button % (
            reverse('planet:feed-unsubscribe', kwargs={'pk': feed.pk}),
            _('Unsubscribe from Feed'),
            'minus-circle'
        )
        refresh_button = self.button % (
            reverse('planet:feed-refresh', kwargs={'pk': feed.pk}),
            _('Refresh Feed'),
            'sync'
        )
        update_button = self.button % (
            reverse('planet:feed-update', kwargs={'pk': feed.pk}),
            _('Update Feed'),
            'edit'
        )
        delete_button = self.button % (
            reverse('planet:feed-delete', kwargs={'pk': feed.pk}),
            _('Delete Feed'),
            'trash-alt'
        )
        options_dialog = self.button % (
            reverse('planet:options'),
            _('User Options'),
            'cog',
        )

        result = view_button
        is_subscribed = False
        if user is not AnonymousUser and user.is_authenticated:
            try:
                opt = Options.objects.get(user=user)
                is_subscribed = \
                    Subscription.objects.filter(user=opt, feed=feed).exists()
            except Options.DoesNotExist:
                result += options_dialog
            if user.has_perm('can_subscribe', feed):
                if is_subscribed:
                    result += unsubscribe_button
                else:
                    result += subscribe_button
            if user.has_perm('can_refresh_feed', feed):
                result += refresh_button
            if user.has_perm('change_feed', feed):
                result += update_button
            if user.has_perm('delete_feed', feed):
                result += delete_button
        return result


@register.tag('feed_controls')
def feed_controls(parser, token):
    """
    recent_posts
    ============

    Templatetag to render controls for a feed.
    Controls are:

    """
    try:
        tag_name, feed = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires one arguments" %
            token.contents.split()[0]
        )
    return FeedControlsNode(feed)


class PostSocialNode(template.Node):
    """
    renders social values for a post object.
    """
    def __init__(self, post):
        self.post = template.Variable(post)

    def render(self, context):
        try:
            post = self.post.resolve(context)
        except Post.MultipleObjectsReturned:
            raise template.TemplateSyntaxError(
                """
                'social' template tag requires 'post' as first argument.
                Got this instead:
                %r (type: %r)
                """ %
                self.post, type(self.post)
            )

        result = """
  <div class="row">
    <div class="col-md-2"><span class="label label-primary">Tweets</span></div>
    <div class="col-md-2"><span class="label label-primary">Blogs</span></div>
    <div class="col-md-2"><span class="label label-primary">Likes</span></div>
    <div class="col-md-2"><span class="label label-primary">Shares</span></div>
  </div> <!-- /row -->
  <div class="row">
    <div class="col-md-2">
        <center><strong>
        %s<meta itemprop="interactionCount" content="UserTweets:%s"/>
        </strong></center>
    </div>
    <div class="col-md-2">
        <center><strong>
        %s
        </strong></center>
    </div>
    <div class="col-md-2">
        <center><strong>
        %s<meta itemprop="interactionCount" content="UserLikes:%s"/>
        </strong></center>
    </div>
    <div class="col-md-2"><center><strong>%s</strong></center></div>
  </div> <!-- /row -->
  <div class="row">
    <div class="col-md-2"><span class="label label-primary">Plus1</span></div>
    <div class="col-md-2"><span class="label label-primary">Views</span></div>
    <div class="col-md-2"><span class="label">xxx</span></div>
    <div class="col-md-2"><span class="label">xxx</span></div>
  </div> <!-- /row -->
  <div class="row">
    <div class="col-md-2">
        <center><strong>
        %s<meta itemprop="interactionCount" content="UserPlusOnes:%s"/>
        </strong></center>
    </div>
    <div class="col-md-2"><center><strong>%s</strong></center></div>
  </div> <!-- /row -->
        """ % (
            post.tweets,
            post.tweets,
            post.blogs,
            post.likes,
            post.likes,
            post.shares,
            post.plus1,
            post.plus1,
            post.pageviews,
        )
        return result


@register.tag('social')
def social(parser, token):
    """
    social
    ============

    social values for a post
    """
    try:
        tag_name, post = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires one arguments" %
            token.contents.split()[0]
        )
    return PostSocialNode(post)


class Top5Node(template.Node):
    def __init__(self, interval, var_name):
        if "daily" in interval:
            self.interval = datetime.now() - timedelta(days=1)
        else:
            raise NotImplementedError
        self.var_name = var_name

    def render(self, context):
        top5 = Post.objects.filter(
            published__gt=self.interval
        ).order_by('-score')
        context[self.var_name] = top5[:5]


@register.tag('top5')
def top5(parser, token):
    """
    top5
    ============

    top 5 post in interval
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires one arguments" %
            token.contents.split()[0]
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    interval, var_name = m.groups()
    return Top5Node(interval, var_name)
