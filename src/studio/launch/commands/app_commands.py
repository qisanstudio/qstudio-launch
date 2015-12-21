# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import sh
import time
import json
import importlib
from sh import pip
from termcolor import colored
from studio.frame.config import common as common_config
from studio.launch.base import manager

app_manager = manager.subcommand('app')
VASSALS = common_config['UWSGI_EMPEROR']


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
    config_d = {}
    for k, v in config.items():
        if k.startswith('UWSGI_'):
            k = k[6:].replace('_', '-').lower()
            config_d[k] = v

    return config_d


def _register(appname, **config_d):
    vassals_dir = VASSALS
    try:
        os.makedirs(vassals_dir)
    except OSError:
        pass
    uwsgi_cfg = {}
    uwsgi_cfg.setdefault('env', []).extend([
                                           #        'STUDIO_ENVIRON=%s' % common_config['ENVIRON'],
                                           'STUDIO_APPNAME=%s' % appname])
    uwsgi_cfg.update(config_d)
    print('Registering app %s:' % appname, end=' ')
    with open(os.path.join(vassals_dir,
                           '%s.json' % appname), 'wb') as fp:
        json.dump({'uwsgi': uwsgi_cfg}, fp)
    print(colored('ok', 'green', attrs=['bold']) + '.')


@app_manager.command
def add(*appnames):
    _names = _get_appnames()
    for appname in appnames:
        if appname in _names:
            app = _get_app(appname)
            config_d = _mk_uwsgi_config(app.config)
            _register(appname, **config_d)


@app_manager.command
def touch(*apps):
    for appname in apps:
        vassal = appname + '.json'
        path = os.path.join(VASSALS, vassal)
        if not os.path.exists(path):
            print(colored('App %s not added, ignored.' % appname,
                          'yellow', attrs=['bold']),
                  file=sys.stderr)
        else:
            print('Touching %s:' % appname, end=' ')
            sh.touch(path)
            print(colored('ok', 'green', attrs=['bold']) + '.')
            time.sleep(1)
