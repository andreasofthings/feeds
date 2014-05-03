#! /usr/bin/env

import os
import sys
import argparse
from django.conf import settings

class DjangoTest(object):
    """
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'crispy_forms',
        'feeds',
        'test',
    )

    def __init__(self, *args, **kwargs):
        """
        Test Django App for Django 1.5 in travis.ci
        """
        self.apps = args
        settings.configure(
            DEBUG = True,
            ROOT_URLCONF = "test.urls",
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'myapp_test',
                    'USER': 'root',
                    'PASSWORD': '',
                    'HOST': 'localhost',
                    'PORT': '',
                }
            },
            INSTALLED_APPS = self.INSTALLED_APPS + self.apps
        )
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner().run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

if __name__ == '__main__':
    """
    """
    DjangoTest('feeds')
