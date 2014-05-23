#! /usr/bin/env

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


if __name__ == '__main__':
    """
    Test Django App in travis.ci
    """
    import django
    if hasattr(django, 'setup'):
        django.setup()
    from django.test.runner import DiscoverRunner
    failures = DiscoverRunner().run_tests(("feeds",), verbosity=1)
    if failures:
        sys.exit(failures)
