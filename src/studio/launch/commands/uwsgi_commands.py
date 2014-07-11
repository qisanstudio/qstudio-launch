# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import sh
import baker
from sh import uwsgi


@baker.command
def _uwsgi_start(*apps):
    uwsgi()

