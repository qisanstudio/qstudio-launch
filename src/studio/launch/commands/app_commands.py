# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import importlib
from sh import pip
from termcolor import colored
from studio.frame.config import common as common_config
from studio.launch.base import manager

app_manager = manager.subcommand('app')
VASSAL = common_config['UWSGI_EMPEROR']

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


def _iter_all():
    for pkg in pip.freeze():
        appname, _ = pkg.split('==')
        if 'microsite' == appname:
            yield appname


def _get_pkgs():
    return [str(pkg.split('==')[0]) for pkg in pip.freeze()]


def _get_appnames():
    pkgs = _get_pkgs()
    return [pkg[6:] for pkg in pkgs if pkg.startswith('qsapp-')]


def _mk_uwsgi_config(config):
    conifg_d = {}
    for k, v in config.items():
        if k.startswith('UWSGI_'):
            k = k[6:].replace('_', '-')
            conifg_d[k] = v
    print(VASSAL)


@app_manager.command
def add(*appnames):
    _names = _get_appnames()
    for appname in appnames:
        if appname in _names:
            app = _get_app(appname)
            _mk_uwsgi_config(app.config)
