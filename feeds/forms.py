#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Button, Div
from crispy_forms.bootstrap import FormActions
from django.core import validators
from django.core.exceptions import ValidationError

from exceptions import Exception
from bs4 import BeautifulSoup
import requests

from feeds.models import Site, Feed, Category, Tag

class SiteValidator(validators.URLValidator):
    def __init__(self, *args, **kwargs):
        super(SiteValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        try:
            super(SiteValidator, self).__call__(value)
        except ValidationError as e:
            raise

        try:
            html = requests.get(value)
            soup = BeautifulSoup(html.text)
            result = []
            for link in soup.head.find_all('link'):
                if "application/rss" in link.get('type'):
                    result.append(link.get('href'))
            if not results:
                raise Exception
        except Exception:
            raise 
        else:
            site = value

class SiteField(forms.URLField):
    default_validators = [SiteValidator]

    def __init__(self, *args, **kwargs):
        super(SiteField, self).__init__(*args, **kwargs)

class SiteCreateForm(forms.ModelForm):
    """
    Form to create a new Site
    """
    url = SiteField()
    class Meta:
        model = Site
        fields = ('url', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'planet:site-add'
        self.helper.layout = Layout(
            Field('url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        super(SiteCreateForm, self).__init__(*args, **kwargs)

class SiteFeedAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SiteFeedAddForm, self).__init__(*args, **kwargs)

class SiteUpdateForm(forms.ModelForm):
    """
    Form to update an existing Site
    """
    class Meta:
        model = Site
        fields = ('url', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'planet:site-update'
        self.helper.layout = Layout(
            Field('url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        super(SiteUpdateForm, self).__init__(*args, **kwargs)

class FeedCreateForm(forms.ModelForm):
    """
    FeedCreateForm

    Django Form to create an angryplanet-feed

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    class Meta:
        model = Feed
        fields = ('name', 'shortname', 'feed_url', 'category',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Add Feed',
                'feed_url',
                'name',
                'shortname',
                'category',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        self.helper.form_action = 'planet:feed-add'
        super(FeedCreateForm, self).__init__(*args, **kwargs)

class FeedUpdateForm(forms.ModelForm):
    """
    FeedUpdateForm

    Django Form to modify an angryplanet-feed

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    class Meta:
        model = Feed
        fields = ('name', 'shortname', 'feed_url', 'category',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Add Feed',
                'name',
                'shortname',
                'feed_url',
                'category',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        # self.helper.form_action = 'planet:feed-update'
        super(FeedUpdateForm, self).__init__(*args, **kwargs)

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'parent',)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'title', 
                'parent',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = 'planet:category-add'
        super(CategoryCreateForm, self).__init__(*args, **kwargs)

class CategoryUpdateForm(forms.ModelForm):
    """
    CategoryUpdateForm

    Django Form to modify an angryplanet-category

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    class Meta:
        model = Category
        fields = ('title', 'slug', 'parent',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Change Category',
                'title',
                'slug',
                'parent',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)


class TagCreateForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('name', )

class FeedAdminForm(forms.ModelForm):
  class Meta:
    model = Feed
