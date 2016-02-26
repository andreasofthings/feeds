#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
helper functions for angryplanet.feeds
"""

import sys
import time
import datetime
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
    links = []

    def handle_starttag(self, tag, attrs):
        if "link" in tag:
            attr = {}
            for k, v in attrs:
                attr[k] = v
            self.links.append(attr)

    @property
    def get_links(self):
        return self.links


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


def getText(nodelist):
    """
    get Text from nodes in XML structures
    """
    Result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            Result.append(node.data)
    return ''.join(Result)


def encode(tstr):
    """
    Encodes a unicode string in utf-8
    """
    if not tstr:
        return ''
    # this is _not_ pretty, but it works
    try:
        return tstr.encode('utf-8', "xmlcharrefreplace")
    except UnicodeDecodeError:
        # it's already UTF8.. sigh
        return tstr.decode('utf-8').encode('utf-8')


def prints(tstr):
    """
    lovely unicode
    """
    sys.stdout.write(
        '%s\n' % (
            tstr.encode(
                sys.getdefaultencoding(),
                'replace'))
        )
    sys.stdout.flush()


def mtime(ttime):
    """
    datetime auxiliar function.
    """
    if type(ttime) == 'str':
        argtime = time.localtime(ttime.split())
    else:
        argtime = ttime

    try:
        mktime = time.mktime(argtime)
    except TypeError as e:
        raise e

    try:
        return datetime.datetime.fromtimestamp(mktime)
    except Exception as e:
        raise e


# vim: ts=4 et sw=4 sts=4
