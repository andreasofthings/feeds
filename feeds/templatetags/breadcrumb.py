#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import template

register = template.Library()

template = """
<ol class="breadcrumb">
</ol>"""
item = """<li class="breadcrumb-item"><a href="#">Home</a></li>"""
active_item = """<li class="breadcrumb-item active">Data</li>"""


@register.simple_tag(name="breadcrumb", takes_context=True)
def breadcrumb(context, argument):
    return template
