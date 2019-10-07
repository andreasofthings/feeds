from django.db import models


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
