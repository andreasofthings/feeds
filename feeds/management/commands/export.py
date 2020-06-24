"""
Export Management Command.

Export `feeds` content for external processing.
"""

import time
import logging

from django.core.management.base import BaseCommand, CommandError
import feedparser

from feeds.models import Post


class Command(BaseCommand):
    help = "export feeds and posts"

    def handle(self, *args, **options):
        feed = Post.objects.all()
        logging.debug(f"Exporting {Post.objects.count()} posts.")
