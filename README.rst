=====
Feeds
=====

.. image:: https://travis-ci.org/aneumeier/feeds.png?branch=master
   :target: https://travis-ci.org/aneumeier/feeds

.. image:: https://coveralls.io/repos/aneumeier/feeds/badge.png
   :target: https://coveralls.io/r/aneumeier/feeds

.. image:: https://readthedocs.org/projects/feeds/badge/?version=latest
  :target: https://readthedocs.org/projects/feeds/?badge=latest
  :alt: Documentation Status


.. image::http://app.review.ninja/assets/images/wereviewninja-32.png
   :target: http://app.review.ninja/aneumeier/feeds



Feeds aims to be a feed aggregator, readed and potentially a replacement for feedburner_.

It is realized as a Django app. It takes feeds in any format `feedparser` can understand and aims to reproduce identical but trackable feeds, augmented with feedbrater information.

Source for Documentation_ is in the "docs" directory.

Quick start
-----------

1. Add "feeds" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'feeds',
      )

2a. Include the feeds URLconf in your project urls.py like this::

            url(r'^feeds/', include( 'feeds.urls', namespace="planet", app_name="planet")),

   Mind the namespace.

2b. For the API, also include the following URLs::

              url(r'^feedapi/', include('feeds.api_urls')),

In this case, mind the absence of an namespace.


3. Run `python manage.py syncdb` to create the feeds models.


.. _Documentation: http://feeds.readthedocs.org/en/latest/
.. _feedburner: http://www.feedburner.com
.. _buildbot: https://angry-planet.com/buildbot
