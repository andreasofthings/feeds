#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Serializers for the Feeds API
"""

from rest_framework import serializers
from ..models import Options, WebSite, Feed, Post, Subscription, Category, Tag


class OptionsSerializer(serializers.ModelSerializer):
    """
    Serializer for User Options

    .. classauthor:: Andreas Neumeier
    """
    class Meta:
        model = Options
        fields = (
            "pk",
            "user",
            "number_initially_displayed",
        )


class WebSiteSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize WebSite Models."""

    class Meta:
        """Serializer Meta."""

        model = WebSite
        fields = (
            'pk',
            'website_url',
            'slug',
            'feeds',
        )
        extra_kwargs = {
            'url': {'view_name': 'planet:website-api-detail', },
            'feeds': {
                'lookup_field': 'pk',
                'view_name': 'planet:feed-api-detail'
            }
        }


class FeedPKSerializer(serializers.Serializer):
    """Serializer for Feed PK."""

    pk = serializers.IntegerField(min_value=0)

    class Meta:
        """Meta for FeedPKSerializer."""

        fields = (
            'pk',
        )


class FeedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        """
            'get_absolute_url',
            'feed_url',
            'name',
            'short_name',
            'slug',
            'is_active',
            'title',
            'link',
            'tagline',
            'language',
            'copyright',
            'author',
            'webmaster',
        """
        model = Feed
        fields = (
            'pk',
            'url',
            'feed_url',
            'name',
            'posts',
        )
        extra_kwargs = {
            'url': {'view_name': 'planet:feed-api-detail', },
            'posts': {
                'lookup_field': 'pk',
                'view_name': 'planet:post-api-detail',
            }
        }


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'url',
            'feed',
            'title',
            'link',
            'published',
            'categories',
            'tags',
        )
        extra_kwargs = {
            'url': {'view_name': 'planet:post-api-detail', },
            'categories': {
                'lookup_field': 'pk',
                'view_name': 'planet:category-api-detail'
                },
            'tags': {
                'lookup_field': 'pk',
                'view_name': 'planet:tag-api-detail'
                },
            'feed': {
                'lookup_field': 'pk',
                'view_name': 'planet:feed-api-detail'
            }
        }


class CategorySerializer(serializers.ModelSerializer):
    """
    Serialize Category.

    """

    class Meta:
        """Meta CatgeorySerializer."""

        model = Category
        fields = ('name', 'url', 'category_feeds', 'categories', )
        extra_kwargs = {
            'url': {'view_name': 'planet:category-api-detail', },
            # 'category_feeds': {'view_name': 'planet:feed-api-detail', },
        }


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Tag.

    """

    class Meta:
        """Meta CatgeorySerializer."""

        model = Tag
        fields = ('name', 'url', )
        extra_kwargs = {
            'url': {'view_name': 'planet:tag-api-detail', },
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Seriaize Subscriptions.

    """

    class Meta:
        """Meta UserSubscriptionsSerializer."""

        model = Subscription
        fields = (
            'pk',
            'user',
            'feed'
        )
