from rest_framework import serializers
from category.models import Category

from ..models import WebSite, Feed, Post


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = (
            'pk',
            'url',
            'get_absolute_url',
            'website',
            'feed_url',
            'name',
            'short_name',
            'slug',
            'is_active',
            'errors',
            'category',
            'title',
            'link',
            'tagline',
            'language',
            'copyright',
            'author',
            'webmaster',
            'pubDate',
            'last_modified',
            'ttl',
            'image_title',
            'image_link',
            'image_url',
            'etag',
            'last_checked',
            'check_interval',
        )


class WebSiteSerializer(serializers.HyperlinkedModelSerializer):
    # feeds = FeedSerializer(required=True)
    class Meta:
        model = WebSite
        fields = (
            'pk',
            'url',
            'slug',
            'feeds',
        )


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
        model = Feed
        fields = ('name', )
