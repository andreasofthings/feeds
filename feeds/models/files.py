#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FileModel(models.Model):
    """
    Model to hold a file.
    """
    data = models.FileField(_('data'))

    def __unicode__(self):
        return u'%s' % (self.title)
