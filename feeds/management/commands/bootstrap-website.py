import logging
import yaml
from urllib.parse import urlparse
from urllib.request import urlopen

import requests
from django.core.management.base import BaseCommand, CommandError

from feeds.models import WebSite
from feeds.tools import getFeedsFromSite
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    bootstrap-website.

    Fetches a list of `websites` from remote directory and adds them to the
    local website-store.

    Args:
       Comes with a default url, but will accept `_latest`, a
       URL containing a YAML.

    Returns:
       type: None.

    Raises:
       Exception: description

    """

    help = "bootstrap a site"

    _latest = \
    "https://raw.githubusercontent.com/andreasofthings/directory/master/README.yaml"

    def _list(self, _latest):
        with urlopen(_latest) as urls:
            urlreader = yaml.load(urls)
            for url in urlreader['Links']:
                yield (urlparse(url['Link']).geturl(), url.get('Name', None))


    def handle(self, *args, **options):
        # site is a tuple of (url, name)
        for url, name in self._list(self._latest):
            scheme, netloc, path, params, query, fragment = \
            urlparse(url)
            if not path: path = "/"
            try:
                w = WebSite.objects.get(netloc=netloc, path=path)
            except ObjectDoesNotExist:
                w = WebSiteobjects.create_website(url, name)
            w.save()
