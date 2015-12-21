# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import abort, redirect, url_for
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask.ext.login import LoginManager, current_user

from .. import app


ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
login_manager = LoginManager()


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_anonymous:
                return redirect(url_for('views.login'))
            user_roles = set([r.name for r in current_user.roles])
            if not set(roles).issubset(user_roles):
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
