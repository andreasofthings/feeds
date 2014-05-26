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
from crispy_forms.layout import Div
from crispy_forms.bootstrap import FormActions

from feeds.models import Options
from feeds.models import Site
from feeds.models import Feed
from feeds.models import Category
from feeds.models import Tag

from feeds.validators import SiteField, FeedField


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
        super(OptionsForm, self).__init__(*args, **kwargs)


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
            Field('opml'),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        super(OPMLForm, self).__init__(*args, **kwargs)


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
        self.helper.form_class = "field_inline"
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


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)

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
    """
    """
    class Meta:
        model = Tag
        fields = ('name', )


class FeedAdminForm(forms.ModelForm):
    class Meta:
        exclude = ()
        model = Feed
