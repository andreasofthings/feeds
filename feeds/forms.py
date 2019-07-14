#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from urllib.parse import urlparse

from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Submit
from crispy_forms.layout import Button
from crispy_forms.layout import Div
from crispy_forms.bootstrap import FormActions
from django.core.exceptions import ValidationError

from .models import Category
from .models import Tag
from .models import Options
from .models import WebSite
from .models import Feed

from .validators import WebSiteField, FeedField


class OptionsForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = (
            'number_initially_displayed',
            'number_additionally_displayed',
            'max_entries_saved',
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "field_inline"
        self.helper.form_action = 'planet:options'
        self.helper.layout = Layout(
            Field('number_initially_displayed'),
            Field('number_additionally_displayed'),
            Field('max_entries_saved'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        return super(OptionsForm, self).__init__(*args, **kwargs)


class OPMLForm(forms.Form):
    """
    Form that shall allow upload of OPML Files.
    """
    opml = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "field_inline"
        self.helper.form_action = 'planet:opml'
        self.helper.layout = Layout(
            Fieldset(
                'Import OPML.',
                'opml'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-mini'),
                Button('cancel', 'Cancel', css_class='btn btn-mini')
            )
        )
        super(OPMLForm, self).__init__(*args, **kwargs)


class WebSiteCreateForm(forms.ModelForm):
    """
    Form to create a new Site
    """

    website_url = WebSiteField()

    def save(self, commit=True):
        data = self.cleaned_data
        try:
            scheme, netloc, path, params, query, fragment = \
                urlparse(data['website_url'])
        except ValidationError as e:
            raise ValidationError(e)

        self.instance.scheme = scheme
        self.instance.netloc = netloc
        self.instance.path = path
        self.instance.params = params
        self.instance.query = query
        self.instance.fragment = fragment
        return super(WebSiteCreateForm, self).save(commit)

    class Meta:
        model = WebSite
        fields = ('website_url', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "field_inline"
        self.helper.form_action = 'planet:website-add'
        self.helper.layout = Layout(
            Field('website_url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        super(WebSiteCreateForm, self).__init__(*args, **kwargs)


class FeedAddForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ("feed_url", )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "field_inline"
        self.helper.form_action = 'planet:feed-add'
        self.helper.layout = Layout(
            FormActions(
                Submit(
                    'submit',
                    'Add',
                    css_class=
                    'btn btn-sm btn-outline-secondary'
                    ),
            )
        )
        super(FeedAddForm, self).__init__(*args, **kwargs)


class WebSiteFeedAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(WebSiteFeedAddForm, self).__init__(*args, **kwargs)


class WebSiteUpdateForm(forms.ModelForm):
    """
    Form to update an existing Site
    """
    class Meta:
        model = WebSite
        exclude = ('website_url', )
        fields = ('scheme', 'netloc', 'path')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'planet:website-update'
        """
        self.helper.layout = Layout(
            # Field('website_url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        """
        super(WebSiteUpdateForm, self).__init__(*args, **kwargs)


class FeedCreateForm(forms.ModelForm):
    """
    FeedCreateForm

    Django Form to create an angryplanet-feed

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    feed_url = FeedField()

    class Meta:
        model = Feed
        fields = ('name', 'short_name', 'feed_url', 'category',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Add Feed',
                'feed_url',
                'name',
                'short_name',
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
        fields = ('name', 'short_name', 'feed_url', 'category',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Add Feed',
                'name',
                'short_name',
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


class FeedAdminForm(forms.ModelForm):
    class Meta:
        exclude = ()
        model = Feed


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'name',
                'parent',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-sm'),
                Button('cancel', 'Cancel', css_class='btn-sm')
            )
        )
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = reverse('planet:category-add')
        super(CategoryCreateForm, self).__init__(*args, **kwargs)


class CategoryUpdateForm(forms.ModelForm):
    """
    CategoryUpdateForm

    Django Form to modify an angryplanet-category

    ..author: Andreas Neumeier
    """
    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Change Category',
                'name',
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


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)
