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

    def get_by_natural_key(self, slug):
        """
        Get natural key

        To allow serialization by key rather than `pk`
        """

        return self.get(slug=slug)
