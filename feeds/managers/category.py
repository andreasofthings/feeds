import logging
from django.db import models
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):
    """
    Manage Category Objects.

    .
    """

    def forPost(self, *args, **kwargs):
        post = kwargs['post']
        tags = kwargs['tags']
        """List {'term': 'Harm Reduction', 'scheme': None, 'label': None}"""
        for tag in tags:
            t, created = self.get_or_create(
                name=tag['term'],
                slug=slugify(tag['term'])
            )
            post.tags.add(t)
        # logger.error("Tag: %s - %s", t, created)
        return

    def forPost(self, *args, **kwargs):
        post = kwargs['post']
        categories = kwargs['categories']
        print(type(categories))

        for category in categories:
            print(category)
            c, created = self.get_or_create(
                name=category,
                slug=slugify(category)
            )
            post.categories.add(c)

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)
