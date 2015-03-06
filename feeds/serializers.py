from rest_framework import serializers
from .models import Feed, Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('name', )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('name', )
