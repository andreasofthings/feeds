from haystack import indexes
from .models import Feed, Post
from category.models import Category, Tag


class FeedIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField()
    short_name = indexes.CharField()
    tagline = indexes.CharField()

    def get_model(self):
        return Feed


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class TagIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()

    def get_model(self):
        return Tag


class CategoryIndex(indexes.SearchIndex):
    name = indexes.CharField(document=True, use_template=True)
    slug = indexes.CharField()

    def get_model(self):
        return Category
