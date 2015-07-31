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
    except ValueError:
        logger.error(json.dumps(params))
        logger.error(headers)
    except:
        logger.debug("stop: counting +1s. Got none. Something weird happened.")

    if resp.status_code == 200:
        result = json.loads(resp.text)
        try:
            post.plus1 = int(
                result['result']['metadata']['globalCounts']['count']
            )
            post.save()
            logger.debug("stop: counting +1s. Got %s.", post.plus1)
            return post.plus1
        except KeyError as e:
            raise KeyError(e)
