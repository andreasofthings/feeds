#! /usr/bin/env python

import os
import sys

if 'TRAVIS' in os.environ:
    import MySQLdb
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.travis-settings'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

if __name__ == '__main__':
    """
    Test Django App in travis.ci
    """
    import django
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], "makemigrations", "feeds"])
    execute_from_command_line([sys.argv[0], "migrate"])
    if hasattr(django, 'setup'):
        django.setup()
    from django.test.runner import DiscoverRunner
    failures = None
    try:
        failures = DiscoverRunner().run_tests(("feeds",), verbosity=2)
    except MySQLdb.OperationalError, e:
        if e[0] == 2006:
            print("MySQL has gone away.")
        else:
            raise MySQLdb.OperationalError(e)
    if failures:
        sys.exit(failures)
