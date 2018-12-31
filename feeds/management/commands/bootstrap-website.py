from django.core.management.base import BaseCommand, CommandError
import requests
import yaml
from time import sleep
from feeds.models import WebSite
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "bootstrap a site"

    def handle(self, *args, **options):
        from feeds.tools import getFeedsFromSite
        from feeds.tools import URLlist

        for site in URLlist():
            try:
                WebSite.objects.create_website(site)
            except Exception as e:
                logger.error("%s raised %s", site, e)
            logger.info(site)
