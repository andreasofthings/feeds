import logging
from django.db import models
from django.utils.text import slugify

logger = logging.getLogger(__name__)


class EditorCategoryManager(models.Manager):
    """
    Manage Category Objects.

    As opposed to the `CategoryManager`, this one
    is restricted to Editor use and will not auto updated
    with refreshed `Posts`.
    """

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)
