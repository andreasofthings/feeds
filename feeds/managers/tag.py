import logging
from django.db import models
from django.utils.text import slugify

import feeds

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
            term = tag['term']
            try:
                t = self.get(
                    name=term,
                    slug=slugify(term),
                )
            except feeds.models.category.Tag.DoesNotExist as e:
                t = self.create(name=term, slug=slugify(term))
                t.save()
                logger.info(f"Tag '{term}' did not exist, created {t}({t.id}).")
            # except Exception as e:
                # import sys, traceback
                # exc_type, exc_value, exc_traceback = sys.exc_info()
                # traceback.print_exc(limit=2, file=sys.stdout)
        post.tags.add(t)
        post.save()

    def get_by_natural_key(self, slug):
        """
        Get natural key

        To allow serialization by key rather than `pk`
        """

        return self.get(slug=slug)
