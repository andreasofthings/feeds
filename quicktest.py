#! /usr/bin/env

import os
import sys
import argparse
from django.conf import settings

class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.

    Example usage:

        >>> QuickDjangoTest('app1', 'app2')

    Based on a script published by Lukasz Dziedzia at: 
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'crispy_forms',
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
    What do when the user hits this file from the shell.

    Example usage:

        $ python quicktest.py app1 app2

    """
    parser = argparse.ArgumentParser(
        usage="[args]",
        description="Run Django tests on the provided applications."
    )
    parser.add_argument('apps', nargs='+', type=str)
    args = parser.parse_args()
    QuickDjangoTest(*args.apps)
