"""
category manager.

Manages Category Objects.
"""
import logging
from django.db import models
from django.utils.text import slugify

import feeds

logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):
    """
    Manage Category Objects.

    .
    """

    def forPost(self, *args, **kwargs):
        post = kwargs['post']
        categories = kwargs['categories']

        for category in categories:
            slug=slugify(category)
            try:
                cat = self.get(
                    name=category,
                    slug=slug,
                    # parent=None
                )
            except feeds.models.category.Category.DoesNotExist as e:
                cat, c = self.get_or_create(
                    name=category,
                    slug=slug,
                    # parent=None,
                )
                cat.save()
                logger.info(f"Category '{category}' did not exist, created {cat}({cat.id}).")
            post.categories.add(cat)

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)
