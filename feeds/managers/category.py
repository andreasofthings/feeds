from django.db import models
from django.utils.text import slugify

class CategoryManager(models.Manager):
    """
    Manage Category Objects.

    .
    """

    def get_by_natural_key(self, slug):
        """
        Allow Get by Key.

        Get Category by natural key to allow serialization. In this case,
        the key is the `slug`.
        """

        return self.get(slug=slug)

    def fromFeedparser(self, *args, **kwargs):
        post = kwargs['post']
        entry = kwargs['entry']
        if 'category' in entry and len(entry.category) > 0:
            for category in entry.category:
                category, created = self.get_or_create(
                    post=post,
                    name=entry.category,
                    slug=slugify(entry.category)
                )
            return
