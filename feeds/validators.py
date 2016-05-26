from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


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


class WebSiteValidator(validators.URLValidator):
    """
    WebSiteValidator
    =============

    Supposed to validate a site to contain a feed.

    .. todo: actually validate the site.
    To do so, use the `:py:function:tools.getFeedsFromSite` function.
    """
    def __init__(self, *args, **kwargs):
        super(WebSiteValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        try:
            super(WebSiteValidator, self).__call__(value)
        except ValidationError as e:
            raise e

        self.site = value


class WebSiteField(forms.URLField):
    default_validators = [WebSiteValidator]

    def __init__(self, *args, **kwargs):
        super(WebSiteField, self).__init__(*args, **kwargs)
