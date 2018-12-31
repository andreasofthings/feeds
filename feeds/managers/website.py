#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
WebSiteManager
==============
"""

from django.db import models


class WebSiteManager(models.Manager):
    """
    :py:mod:`WebSiteManager` provide extra functions.
    """

    def __init__(self, *args, **kwargs):
        return super(WebSiteManager, self).__init__(*args, **kwargs)

    def create_website(self, website_url):
        from urllib.parse import urlparse
        schema, netloc, path, params, query, fragment = urlparse(website_url)
        website = self.create(
            scheme=schema,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment
        )
        # do something with the book
        return website

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
