#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
OptionsManager
==============
"""

from django.db import models


class OptionsManager(models.Manager):
    def get(self, *args, **kwargs):
        """
        Override get to ensure Options are created if not existing yet.
        """
        obj, created = self.get_or_create(*args, **kwargs)
        if created:
            obj.save()
        return super(OptionsManager, self).get(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        return super(OptionsManager, self).__init__(*args, **kwargs)
