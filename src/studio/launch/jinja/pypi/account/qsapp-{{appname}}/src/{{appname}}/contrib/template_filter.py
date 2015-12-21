# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template_string
from jinja2 import Markup
from ..models import NaviModel


navi_str = '''
{% for channel in navi.channels %}
    <li class=""><a href="{{ channel.url }}">{{ channel.name }}</a></li>
{% endfor %}
'''


def render_navi(navi_id):
    navi = NaviModel.query.get(1)
    return Markup(render_template_string(navi_str, navi=navi))
