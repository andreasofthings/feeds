#! /usr/bin/env

import os
import sys
from django.conf import settings

if __name__ == '__main__':
    """
    Test Django App in travis.ci
    """
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF="test.urls",
        DIRNAME=os.path.dirname(__file__),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sitemaps',
            'crispy_forms',
            'haystack',
            'test',
            'feeds',
        ),
        CRISPY_TEMPLATE_PACK="bootstrap",
        HAYSTACK_CONNECTIONS={
            "default": {
                'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
                'PATH': os.path.join(
                    os.path.dirname(__file__),
                    'whoosh_index'
                ),
            }
        },
        DATABASES={
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
