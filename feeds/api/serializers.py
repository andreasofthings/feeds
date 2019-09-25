#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Serializers for the Feeds API
"""

from rest_framework import serializers
from ..models import Options, WebSite, Feed, Post, Subscription, Category


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
    feeds = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = WebSite
        fields = (
            'pk',
            'website_url',
            'slug',
            'feeds',
        )


class FeedURLSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'feed_url',
            'name',
        )


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

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
            'url': {'view_name': 'planet:feed-detail', }
        }


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'feed',
            'title',
            'link',
            'published',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'url', )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'pk',
            'user',
            'feed'
        )
