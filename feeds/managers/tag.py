import logging
from django.db import models
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class TagManager(models.Manager):
    """
    Manage `Tag` objects.

    Manager object.
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
        return

    def get_by_natural_key(self, slug):
        """
        Get natural key

        To allow serialization by key rather than `pk`
        """

        return self.get(slug=slug)
