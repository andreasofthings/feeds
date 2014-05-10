#! /usr/bin/env

import os
import sys
import argparse
from django.conf import settings

if __name__ == '__main__':
    """
    Test Django App in travis.ci
    """
    settings.configure(
        DEBUG = True,
        ROOT_URLCONF = "test.urls",
        DIRNAME = os.path.dirname(__file__),
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sitemaps',
            'crispy_forms',
            'feeds',
        ),
        CRISPY_TEMPLATE_PACK = "bootstrap",
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'myapp_test',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },
    )
    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner().run_tests(("feeds",), verbosity=1)
    if failures:
        sys.exit(failures)

