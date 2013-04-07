.. feedbrater documentation master file, created by
   sphinx-quickstart on Wed Apr  3 14:03:23 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to feedbrater's documentation!
======================================

Feedbrater aims to be a replacement for feedburner. It is realized as a Django app. It takes feeds in any format `feedparser` can understand and aims to reproduce identical but trackable feeds, augmented with feedbrater information.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "feeds" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'feeds',
      )

      2. Include the feeds URLconf in your project urls.py like this::

            url(r'^feeds/', include( 'feeds.urls', namespace="planet", app_name="planet")),

         Mind the namespace.

      3. Run `python manage.py syncdb` to create the feeds models.



Contents:
---------

.. toctree::
   :maxdepth: 2

   feeds
   feed_views
   feed_rss
   feed_models
   feed_tasks
   feed_forms
   feed_mixins

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

