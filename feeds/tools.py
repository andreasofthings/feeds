#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
helper functions for angryplanet.feeds
"""

import sys
import time, datetime

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
    sys.stdout.write('%s\n' % (tstr.encode(sys.getdefaultencoding(),
                         'replace')))
    sys.stdout.flush()

def mtime(ttime):
    """ datetime auxiliar function.
    """
    if type(ttime) == 'str':
        argtime = time.localtime(ttime.split())
    else:
        argtime = ttime

    try:
        mktime = time.mktime(argtime)
    except TypeError, e:
        raise e
    
    try:
        return datetime.datetime.fromtimestamp(mktime)
    except Exception, e:
        raise e


# vim: ts=4 et sw=4 sts=4

