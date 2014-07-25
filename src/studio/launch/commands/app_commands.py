# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import importlib

from sh import uwsgi, ErrorReturnCode
from termcolor import colored
from studio.frame import config
from studio.launch.base import manager
from .contrib import build_structure

app_manager = manager.subcommand('app')



def _get_app(appname):
    try:
        module = importlib.import_module(appname)
    except ImportError:
        print(colored('Can\'t import app %s.' % appname,
                      'yellow', attrs=['bold']),
              file=sys.stderr)
        return None

    for name in dir(module):
        app = getattr(module, name)
        if hasattr(app, 'config'):
            return app
    else:
        print(colored('Can\'t find app %s\'s entry' % appname,
                      'yellow', attrs=['bold']),
              file=sys.stderr)
        return None



@app_manager.command
def add(*appnames):
    for appname in appnames:
        app = _get_app(appname)
        print(app.config)
