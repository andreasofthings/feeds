#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
task_time overrides the default celery decorator.
"""

from celery import task
from datetime import datetime

def task_time(*args, **options):
    """
    pass the current time of invocation to the task
    """
    return task(*args, **dict({'invocation_time': datetime.now()}, **options))

# vim: ts=4 et sw=4 sts=4

