from django.core.management.base import BaseCommand, CommandError
import requests
from time import sleep
import logging

from feeds.tools import getFeedsFromSite
from feeds.models import WebSite

logger = logging.getLogger(__name__)
print(__name__)


class Command(BaseCommand):
    help = "bootstrap feedlist"

    def handle(self, *args, **options):

        websites = WebSite.objects.all()

        for site in websites:
            allfeeds = []
            try:
                logger.info("Trying to get Feeds from Site: %s", site)
                allfeeds = getFeedsFromSite(site.website_url)
            except requests.exceptions.SSLError as e:
                logger.error("SSLError: %s", e)
            logger.info("Found %s feeds in %s", len(allfeeds), site)
            for feed in allfeeds:
                # logger.info("Feed: %s", feed)
                pass
            sleep(0.5)
