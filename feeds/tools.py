#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
helper functions for angryplanet.feeds
"""

import requests

try:
    from HTMLParser import HTMLParser as HTMLParser
except:
    from html.parser import HTMLParser as HTMLParser


from typing import TypeVar, Generic, Iterable, Iterator, List


class feedFinder(HTMLParser):
    """
    feedFinder
    ==========

    custom HTMLParser to find all relevant feeds from a website.
    """
    _links = []

    def handle_starttag(self, tag, attrs):
        if "link" in tag:
            attr = {}
            for k, v in attrs:
                attr[k] = v
            self._links.append(attr)

    @property
    def links(self):
        return self._links


def getFeedsFromSite(site):
    """
    Takes 'site' in form of an URL as an Argument.
    Fetches the site, parses it, finds embedded links.
    """
    parser = feedFinder()
    result = []
    html = requests.get(site)
    parser.feed(html.text)
    for link in parser.links:
        if "type" in link.keys():
            if "application/rss" in link['type']:
                result.append((link['title'], link['href']))
    return result

