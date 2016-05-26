from rest_framework import serializers
from .models import Feed, Post
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'url', )


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


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = (
            'name', 
            'feed_url',
            'is_active',
            'category',
            'title',
            'link',
            'tagline',
            'language',
            'copyright',
            'author',
            'webmaster',
            'pubDate',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('name', )
