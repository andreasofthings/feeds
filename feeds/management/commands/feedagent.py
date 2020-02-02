import time
import logging

from django.core.management.base import BaseCommand, CommandError
import feedparser

from feeds.models import Feed


class Command(BaseCommand):
    help = "feedagent to run refresh as a daemon"

    def handle(self, *args, **options):
        feed = Feed.objects.order_by('-last_checked')[0]
        logging.error(f"Count {Feed.objects.count()}")
        while True:
            f = feedparser.parse(feed.feed_url)
            print(f.feed)
            logging.info(f"refreshing feed {feed.title} {feed.name}")
            # logging.info(f"feed detail {f.feed.title}, {f.feed.feed_url}")
            time.sleep(60)
