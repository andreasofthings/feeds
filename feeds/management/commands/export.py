"""
Export Management Command.

Export `feeds` content for external processing.
"""

import time
import logging

from django.core.management.base import BaseCommand, CommandError
import feedparser

from feeds.models import Post

dataset_id = "pramari-de.news"
"""
.. todo::
    Make this configurable via settings.py

"""

class Command(BaseCommand):
    help = "export feeds and posts"

    def handle(self, *args, **options):
        """
        https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries#client-libraries-install-python
        """
        from google.cloud import bigquery
        client = bigquery.Client()
        dataset = bigquery.Dataset(dataset_id)

        # TODO(developer): Specify the geographic location where the dataset should reside.
        dataset.location = "EU"

        try:
            dataset = client.create_dataset(dataset)  # Make an API request.
        except google.api_core.exceptions.Conflict as error:  #  if the Dataset already
            logging.error(error)
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

        posts = Post.objects.all()
        logging.error(f"Exporting {Post.objects.count()} posts.")
