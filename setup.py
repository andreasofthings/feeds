"""
Install feeds.

setup.py for the `feeds` package.
"""

import os
from setuptools import setup
from setuptools.command.install import install
from feeds import __version__

README = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')
) .read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class InstallCommand(install):
    """Customized setuptools install command."""

    def run(self):
        """Run installation first."""
        install.run(self)


setup(
    name='feeds',
    version=__version__,
    packages=['feeds'],
    include_package_data=True,
    license='BSD License',    # example license
    description='A RSS feed aggregator built on Django.',
    long_description=README,
    url='https://pramari.de/feeds',
    author='Andreas.Neumeier',
    author_email='andreas@neumeier.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',    # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django~=3.1.0',
        'django-formtools',
        'django-crispy-forms',
        'djangorestframework~=3.12.0',
        'feedparser',
        'pyyaml',
        'google-cloud',
        'google-cloud-tasks',
        'google-cloud-bigquery',
        'django_haystack>=3.0',
        'django-taggit',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['py.test', ],
    # cmdclass={
    #    'install': InstallCommand,
    # },
)
