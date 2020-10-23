#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
helper functions for angryplanet.feeds
"""

from typing import List, Tuple
import logging
import requests
import yaml

from django.core.cache import cache



try:
    from HTMLParser import HTMLParser as HTMLParser
except ImportError:
    from html.parser import HTMLParser as HTMLParser


# from typing import TypeVar, Generic, Iterable, Iterator, List

logger = logging.getLogger(__name__)


def URLlist():
    """
    Yield all URLs contained in `url`(.yaml)

    See: https://github.com/aneumeier/blogsdirectory/

    .. deprecated:: 1.0
        Don't use this anymore. A new implementation is in
        `feeds/management/commands/bootstrap-website.py`

    .. todo::
        Sort and filter dupes.
    """
    from urllib.parse import urlparse
    from urllib.request import urlopen

    latest = \
    "https://raw.githubusercontent.com/andreasofthings/directory/master/urls.yaml"

    with urlopen(latest) as urls:
        urlreader = yaml.load(urls)
        for url in urlreader['Websites']:
            yield urlparse(url).geturl()


class feedFinder(HTMLParser):
    """
    feedFinder
    ==========

    custom HTMLParser to find all relevant feeds from a website.

    Used in `:py:feeds.tools.getFeedsFromSite`
    """
    _links = []
    _title = ""
    getTitle = False

    def __init__(self):
        self._links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        attr = {}
        if "link" in tag:
            for k, v in attrs:
                attr[k] = v
            self._links.append(attr)
        if tag == 'title':
            self.getTitle = True

    def handle_data(self, data):
        if self.getTitle:
            self._title = data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.getTitle = False

    @property
    def links(self):
        return self._links

    @property
    def title(self):
        return self._title


TitleAndURL = Tuple[str, str]
ListOfTitleAndURL = List[TitleAndURL]


def getFeedsFromSite(site: str) -> ListOfTitleAndURL:
    """
    getFeedsFromSite.

    Take 'site' in form of an URL as an Argument.
    Fetches the site, parses it, finds embedded links.
    """
    from urllib.parse import urlparse, urlunparse
    parser = feedFinder()
    sitecomponents = urlparse(site)

    html = cache.get_or_set(site, requests.get(site), 10600)
    parser.feed(html.text)
    result = []

    links = list(filter(lambda x: "type" in x, parser.links))
    rsslist = list(filter(lambda x: "application/rss" in x['type'], links))

    for link in rsslist:
        feed = link.get('href')
        feedcomponents = urlparse(feed)
        if feedcomponents.netloc in ("", None) or \
            feedcomponents.scheme in ("", None):
            feed = urlunparse((
                sitecomponents.scheme,
                sitecomponents.netloc,
                feedcomponents.path,
                feedcomponents.params,
                feedcomponents.query,
                feedcomponents.fragment)
            )
        result.append((parser.title, feed))

        logger.debug("appended %s to result", feed)
    return result
