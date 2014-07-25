# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import sh
from sh import uwsgi, ErrorReturnCode
from termcolor import colored
from studio.frame import config
from studio.launch.base import manager
from .contrib import build_structure

uwsgi_manager = manager.subcommand('uwsgi')


def _uwsgi_common(*args, **kwargs):
    for key in config.common:
        if not key.startswith('UWSGI_') or \
           key == 'UWSGI_LOGFILE':  # LOGFILE 为特殊配置
            continue
        val = config.common[key]
        if key.startswith('UWSGI_VASSAL_'):
            continue
        else:
            kwargs[key[6:].lower()] = val
#    plugins_dir = config.common['UWSGI_PLUGINS_DIR']
    env = os.environ.copy()
#    env['UWSGI_VASSAL_PLUGINS_DIR'] = plugins_dir
    print(kwargs)
    return uwsgi(_out=sys.stdout, _err=sys.stderr,
                 _env=env,
                 *args, **kwargs)


def is_alive(pidfile):
    if os.path.exists(pidfile):
        with open(pidfile, 'rb') as fp:
            pid = fp.read()
        try:
            sh.kill('-0', pid.strip())
            return True
        except ErrorReturnCode:
            return False
    return False


@uwsgi_manager.command
def start():
    pidfile = config.common['UWSGI_PIDFILE']
    print('Starting uWSGI:', end=' ')
    if is_alive(pidfile):
        print(colored('failed', 'red', attrs=['bold']) +
              ', uWSGI is already running.')
    else:
        _uwsgi_common(daemonize=config.common['UWSGI_LOGFILE'])
        print(colored('uWSGI', 'green', attrs=['bold']) + '.')
