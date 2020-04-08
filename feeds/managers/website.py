#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
WebSiteManager
==============
"""

import logging
from urllib.parse import urlparse
from django.utils.text import slugify
from django.db import models

logger = logging.getLogger(__name__)


class WebSiteManager(models.Manager):
    """
    :py:mod:`WebSiteManager` provide extra functions.
    """

    def __init__(self, *args, **kwargs):
        return super(WebSiteManager, self).__init__(*args, **kwargs)

    def create_website(self, url, name=None, slug=None):
        """
        Create Website.

        Create a new `models.WebSite` from url and name.

        Args:
            url (str): A URL in a parseable, RFC compliant format.
            name (str): A human readable name for the website.

        Returns:
            website: A new Website object.

        """

        scheme, netloc, path, params, query, fragment = \
            urlparse(url)

        if not path: path = "/"
        if not slug:
            def remove_prefix(s, prefix):
                return s[len(prefix):] if s.startswith(prefix) else s
            slug = slugify(netloc + website.path)
            slug = remove_prefix(slug, "https")
            slug = remove_prefix(slug, "http")
            slug = remove_prefix(slug, "www")

        if not name:
            name = slug

        website = self.create(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            name=name,
            slug=slug
        )

        return website

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
