=====
Feedbrater
=====

.. image:: https://travis-ci.org/aneumeier/feedbrater.png?branch=master
   :target: https://travis-ci.org/aneumeier/feedbrater 

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

