from rest_framework import serializers
from .models import Feed, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'url', )


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('name', 'url', )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('name', )
