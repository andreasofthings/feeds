import logging
from django.db import models

logger = logging.getLogger(__name__)


class TagManager(models.Manager):
    """
    Manage `Tag` objects.

    Manager object.
    """

    def forPost(self, *args, **kwargs):
        post = kwargs['post']
        tags = kwargs['tags']
        logger.error("Tags: %s", tags)
        """List {'term': 'Harm Reduction', 'scheme': None, 'label': None}"""
        for tag in tags:
            t, created = self.get_or_create(
                post=post,
                tag=tags['term']
            )
        return

    def get_by_natural_key(self, slug):
        """
        Get natural key

        To allow serialization by key rather than `pk`
        """

        return self.get(slug=slug)
