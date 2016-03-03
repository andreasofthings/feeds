#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
helper functions for angryplanet.feeds
"""

import requests

try:
    from HTMLParser import HTMLParser as HTMLParser
except:
    from html.parser import HTMLParser as HTMLParser


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
    parser = feedFinder()
    result = []
    html = requests.get(site)
    parser.feed(html.text)
    for link in parser.links:
        if "type" in link.keys():
            if "application/rss" in link['type']:
                result.append((link['title'], link['href']))
    return result

# vim: ts=4 et sw=4 sts=4
