#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
social.py
"""

import requests
import json


def tweets(post):
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (post.link)
    resp = requests.get(query)

    if resp.status_code == 200:
        result = json.loads(resp.text)['count']
    return result
