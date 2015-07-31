#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
social.py
"""

import logging
import requests
import json

logger = logging.getLogger(__name__)


def tweets(post):
    """

    """
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (post.link)
    resp = requests.get(query)

    if resp.status_code == 200:
        result = json.loads(resp.text)['count']
    return result


def plusone(post):
    queryurl = "https://clients6.google.com/rpc"
    params = {
        "method": "pos.plusones.get",
        "id": "p",
        "params": {
            "nolog": True,
            "id": "%s" % (post.link),
            "source": "widget",
            "userId": "@viewer",
            "groupId": "@self",
        },
        "jsonrpc": "2.0",
        "key": "p",
        "apiVersion": "v1"
    }
    headers = {
        'Content-type': 'application/json',
    }

    try:
        resp, content = requests.post(
            queryurl,
            data=json.dumps(params),
            headers=headers
            )
        if resp.status_code == 200:
            result_json = json.loads(resp.text)
    except ValueError as e:
        logger.error(e)
        logger.error(json.dumps(params))
        logger.error(headers)
    except Exception as e:
        logger.error("""stop: counting +1s. Something weird happened.\n
                     %s
                     """ % e)

    try:
        result = int(
            result_json['result']['metadata']['globalCounts']['count']
        )
    except KeyError as e:
        raise KeyError(e)

    logger.debug("stop: counting +1s. Got %s.", result)
    return result
