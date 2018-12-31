from django.core.management.base import BaseCommand, CommandError
import requests
import yaml
from time import sleep
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "bootstrap feedlist"

    def handle(self, *args, **options):
        from feeds.tools import getFeedsFromSite
        from feeds.tools import URLlist

        for site in URLlist():
            allfeeds = []
            try:
                logger.info("Trying to get Feeds from Site: %s", site)
                allfeeds = getFeedsFromSite(site)
            except requests.exceptions.SSLError as e:
                logger.error("SSLError: %s", e)
            logger.info("Found %s feeds in %s", len(allfeeds), site)
            for feed in allfeeds:
                # logger.info("Feed: %s", feed)
                pass
            sleep(0.5)
