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
        """
        For every post.

        Un-nest `categories` attached to Post. Store them all separately.
        """
        post = kwargs['post']
        categories = kwargs['categories']

        logger.error(f"Post: {post}")
        logger.error(f"Categories: {categories}")

        for category in categories:
            slug = slugify(category)
            logger.error(f"Have to work with {category} (Slug: {slug}) now.")
            logger.error("Type: {}".format(type(category)))
            try:
                cat = self.get(
                    name=category,
                    slug=slug,
                    )
            except feeds.models.category.Category.DoesNotExist as wtf:
                cat = self.create(
                    name=category,
                    slug=slug,
                    )
                logger.error(f"WTF {wtf}")

            logger.info(f"Category '{category}' did not exist, created {cat}({cat.id}).")
            post.categories.add(cat)

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)
