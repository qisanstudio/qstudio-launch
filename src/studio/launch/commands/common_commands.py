# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import sys
import csv
import time

import sh
from sh import ErrorReturnCode
from pkg_resources import Requirement

from studio.launch.base import manager
from . import (uwsgi_commands, nginx_commands,
               app_commands)


@manager.command
def start():
    nginx_commands.restart()
    uwsgi_commands.start()


@manager.command
def debug():
    try:
        nginx_commands.restart()
        uwsgi_commands.debug()
    finally:
        nginx_commands.reload()


@manager.command
def reload():
    nginx_commands.reload()
    uwsgi_commands.reload()


@manager.command
def stop():
    nginx_commands.stop()
    uwsgi_commands.stop()


@manager.command
def restart():
    nginx_commands.restart()
    uwsgi_commands.restart()


@manager.command
def touch(*app):
    nginx_commands.reload()
    app_commands.touch(*app)
