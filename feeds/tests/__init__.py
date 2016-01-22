#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Tests for the "feeds" app.
==========================

  :date: 2014-05-03
  :version: 0.1
  :description: Test Cases for :py:mod:`feeds`

- :py:mod:`feeds.models`
- :py:mod:`feeds.views`

 - for anonymous users / not logged in
 - for logged in users

- :py:mod:`feeds.tasks`

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>

"""


import pkgutil
import unittest

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)
