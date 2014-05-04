import datetime

from haystack import indexes
from haystack import site
from feeds.models import Feed, Post, Tag


class FeedIndex(indexes.SearchIndex):
    title = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField()
    short_name = indexes.CharField()
    tagline = indexes.CharField()

    def get_model(self):
        return Tag
site.register(Feed, FeedIndex)

class PostIndex(indexes.SearchIndex):
    title = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
site.register(Post, PostIndex)

class TagIndex(indexes.SearchIndex):
    title = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()

    def get_model(self):
        return Tag
site.register(Tag, TagIndex)

