import os
from setuptools import setup
from setuptools.command.install import install
from feeds import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class InstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        """
        Run installation first.
        """
        install.run(self)
        # from django.contrib.auth.models import Group
        # g, created = Group.objects.get_or_create(name="Feeds")
        # if created:
        #     g.save()


setup(
    name='feeds',
    version=__version__,
    packages=['feeds'],
    include_package_data=True,
    license='BSD License',    # example license
    description='A feedburner replacement built on Django.',
    long_description=README,
    url='https://angry-planet.com/feeds',
    author='Andreas.Neumeier',
    author_email='andreas@neumeier.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',    # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'beautifulsoup4>=4.2.1',
        'django-braces>=1.0.0',
        'django-formtools',
        'django-crispy-forms>=1.2.3',
        'feedparser>=5.1.2',
        'requests>=2.2.1,<2.6',
        'django-haystack>=2.3.1',
        'djangorestframework>=3.0.3',
        'elasticsearch==1.4.0',
        'timestring==1.6.2',
        'git+https://github.com/aneumeier/python-django-social.git#latest',
    ],
    # cmdclass={
    #    'install': InstallCommand,
    # },
)
