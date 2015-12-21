# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import redirect, url_for, request
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView


class BaseView(ModelView):

    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        for role in current_user.roles:
            if role.name in ['superadmin', 'admin']:
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('views.login', next=request.url))
