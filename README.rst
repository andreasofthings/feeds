=====
Feeds
=====

.. image:: https://travis-ci.org/andreasofthings/feeds.svg?branch=master
    :target: https://travis-ci.org/andreasofthings/feeds

.. image:: https://coveralls.io/repos/andreasofthings/feeds/badge.png
   :target: https://coveralls.io/r/andreasofthings/feeds

.. image:: https://readthedocs.org/projects/feeds/badge/?version=latest
  :target: https://readthedocs.org/projects/feeds/?badge=latest
  :alt: Documentation Status

.. image:: https://badge.fury.io/py/feeds.svg
    :target: https://badge.fury.io/py/feeds

.. image:: https://requires.io/github/andreasofthings/feeds/requirements.svg?branch=master
     :target: https://requires.io/github/andreasofthings/feeds/requirements/?branch=master
     :alt: Requirements Status

Feeds aims to be a feed aggregator, reader, subscription service, and
potentially a replacement for feedburner_. It is under heavy development and
not in active use. At the time being it serves as a project in code development
and maintenance.

It is realized as a Django app. It takes feeds in any format `feedparser` can
understand and aims to reproduce identical but trackable feeds, augmented with
meta information.

As a side effort, `feeds` queries social media to evaluate the relevance of
individual posts and collects metrics available from the open web, trying
to identify most relevant news.

Source for Documentation_ is in the "docs" directory.

Quick start
-----------

1. Add "feeds" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'feeds',
      )

2. URL configuration

   a. Include the feeds URLconf in your project urls.py like this::


            urlpatterns = patterns(
                '',
                ...
                url(r'^feeds/', include( 'feeds.urls', namespace="planet", app_name="planet")),
            )


      Mind the namespace.

   b. For the API, also include the following URLs::

            urlpatterns = patterns(
                '',
                ...
                url(r'^feeds/', include( 'feeds.urls', namespace="planet", app_name="planet")),
                url(r'^feedapi/', include('feeds.api_urls')),
            )


      In this case, mind the absence of an namespace.


3. Django apps

  Add the following to INSTALLED_APPS, too...

    INSTALLED_APPS = (
      ...
      'crispy_forms',
      'category',
      'haystack',
      )


  `feeds` uses crispy_forms_, category_, haystack_ in it's
  default templates.

4. Run `python manage.py syncdb` to create the feeds models.

5. Other dependencies:

`feeds` may assume it will find the following:

  - /static/bs335 for Bootstrap_.
  - /static/jquery for jquery_.
  - /static/d3 for D3_.

 6. Guidelines

 `feeds` makes an effort to follow best practices and follows PEP8_ and PEP263_
 as a baseline.


.. _Documentation: http://feeds.readthedocs.org/en/latest/
.. _feedburner: http://www.feedburner.com
.. _Bootstrap: http://www.getbootstrap.com
.. _jquery: http://www.jquery.com
.. _D3: http://www.d3js.org
.. _haystack: https://django-haystack.readthedocs.io/en/v2.4.1/
.. _category: https://github.com/aneumeier/category
.. _crispy_forms: http://django-crispy-forms.readthedocs.io/en/latest/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _PEP263: https://www.python.org/dev/peps/pep-0263/
