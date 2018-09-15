from django.core.management.base import BaseCommand, CommandError
import requests
import yaml
from time import sleep
latest = \
    "https://raw.githubusercontent.com/aneumeier/feeds/master/feeds/directory/Websites.yaml"


class Command(BaseCommand):
    help = "bootstrap a site"

    def add_arguments(self, parser):
        parser.add_argument('site', nargs='+', type=str)

    def handle(self, *args, **options):
        from feeds.tools import getFeedsFromSite
        sitetext = requests.get(latest, verify=None).text
        sitelist = yaml.load(sitetext)
        for site in sitelist['Websites']:
            try:
                feeds = getFeedsFromSite(site)
            except requests.exceptions.SSLError:
                continue
            print(site)
            for feed in feeds:
                print(feed)
            sleep(2)
