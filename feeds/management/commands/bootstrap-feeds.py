from django.core.management.base import BaseCommand, CommandError
import requests
from time import sleep
import logging

from feeds.tools import getFeedsFromSite
from feeds.models import WebSite, Feed

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "bootstrap feedlist"

    def handle(self, *args, **options):

        websites = WebSite.objects.all()

        for site in websites:
            allfeeds = []
            try:
                logger.info("Trying to get Feeds from Site: %s", site)
                allfeeds = getFeedsFromSite(site.website_url)
                logger.info(f"found {allfeeds}")

            except requests.exceptions.SSLError as e:
                logger.error(f"SSLError for {site.name}: {e}")
            except requests.exceptions.ConnectionError as e:
                logger.error(f"ConnectionError for {site.name}: {e}")
            for url in allfeeds:
                try:
                    f = Feed.objects.get(feed_url=url)
                except Feed.DoesNotExist:
                    logger.error(f"{url} for {site} is not yet in DB.")
                    f = Feed.objects.create_feed(site, url)
                f.website = site
                f.save()

                # logger.info("Feed: %s", feed)
                # continue
            sleep(0.5)
