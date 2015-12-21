# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import flash
from flask_mail import Mail, Message
from .. import app

mail = Mail(app)


def send_email(email, subject, html):
    if isinstance(email, list):
        recipients = email
    else:
        recipients = [email]
    msg = Message(subject,
                  recipients=recipients,
                  html=html)
    mail.send(msg)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                  getattr(form, field).label.text,
                  error))
