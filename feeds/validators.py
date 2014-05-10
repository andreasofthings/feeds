from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup


class FeedValidator(validators.URLValidator):
    def __init__(self, *args, **kwargs):
        super(FeedValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        import feedparser
        from feedparser import bozo_exception
        try:
            super(FeedValidator, self).__call__(value)
        except ValidationError as e:
            raise e

        try:
            f = feedparser.parse(value)
            f = f.title
        except bozo_exception as e:
            raise e
        else:
            self.feed = value


class FeedField(forms.URLField):
    default_validators = [FeedValidator]

    def __init__(self, *args, **kwargs):
        super(FeedField, self).__init__(*args, **kwargs)


class SiteValidator(validators.URLValidator):
    def __init__(self, *args, **kwargs):
        super(SiteValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        try:
            super(SiteValidator, self).__call__(value)
        except ValidationError as e:
            raise e

        try:
            html = requests.get(value)
            soup = BeautifulSoup(html.text)
            result = []
            for link in soup.head.find_all('link'):
                if "application/rss" in link.get('type'):
                    result.append(link.get('href'))
            if not result:
                raise Exception
        except Exception:
            raise
        else:
            self.site = value


class SiteField(forms.URLField):
    default_validators = [SiteValidator]

    def __init__(self, *args, **kwargs):
        super(SiteField, self).__init__(*args, **kwargs)
