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
        categories = kwargs['categories']
        logger.error("Category: %s", categories)
        for category in categories:
            c, created = self.get_or_create(
                post=post,
                category=category
            )

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)
