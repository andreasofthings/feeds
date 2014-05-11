#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Call a webhook.
"""

import requests

if __name__ == '__main__':
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post(
        "https://angry-planet.com/hook/feeds",
        data=payload,
        verify=False
    )
