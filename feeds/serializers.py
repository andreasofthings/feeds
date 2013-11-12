from rest_framework import serializers
from models import Post

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'tweets', 'likes', 'shares', 'plus1', 'score')
