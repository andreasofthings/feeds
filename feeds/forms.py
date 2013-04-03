#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, Div

from feeds.models import Feed, Category, Tag

class FeedCreateForm(forms.ModelForm):
    """
    FeedCreateForm

    Django Form to create an angryplanet-feed

    ..author: Andreas Neumeier
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
        self.helper.form_action = 'planet:feed-add'
        super(FeedCreateForm, self).__init__(*args, **kwargs)

class FeedUpdateForm(forms.ModelForm):
    """
    FeedUpdateForm

    Django Form to modify an angryplanet-feed

    ..author: Andreas Neumeier
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

    ..author: Andreas Neumeier
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
