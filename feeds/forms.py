#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Submit
from crispy_forms.layout import Button
from crispy_forms.bootstrap import FormActions

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

    url = WebSiteField()

    class Meta:
        model = WebSite
        fields = ('url', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "field_inline"
        self.helper.form_action = 'planet:website-add'
        self.helper.layout = Layout(
            Field('url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        super(WebSiteCreateForm, self).__init__(*args, **kwargs)


class WebSiteFeedAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(WebSiteFeedAddForm, self).__init__(*args, **kwargs)


class WebSiteUpdateForm(forms.ModelForm):
    """
    Form to update an existing Site
    """
    class Meta:
        model = WebSite
        fields = ('url', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'planet:website-update'
        self.helper.layout = Layout(
            Field('url'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
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
