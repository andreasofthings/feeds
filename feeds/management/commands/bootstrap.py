from django.core.management.base import BaseCommand, CommandError
import requests
import yaml

latest = \
    "https://raw.githubusercontent.com/aneumeier/feeds/master/feeds/directory/Websites.yaml"


class Command(BaseCommand):
    help = "bootstrap a site"

    def add_arguments(self, parser):
        parser.add_argument('site', nargs='+', type=str)

    def handle(self, *args, **options):
        sitetext = requests.get(latest).text
        sitelist = yaml.load(sitetext)
        for i in sitelist:
            print(i)
