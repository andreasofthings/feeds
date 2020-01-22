import time
import logging

from django.core.management.base import BaseCommand, CommandError
import feedparser

from feeds.models import Feed


class Command(BaseCommand):
    help = "feedagent to run refresh as a daemon"

    def handle(self, *args, **options):
        while True:
            feed = Feed.objects.order_by('-last_checked')[0]
            f = feedparser.parse(feed.feed_url)
            print(f.feed)
            logging.info("refreshing feed '%s' (%s)", feed.title, feed.name)
            logging.info("feed detail '%s' (%s)", f.feed.title, f.feed.url)
            time.sleep(60)
