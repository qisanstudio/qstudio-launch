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
    env = os.environ.copy()
#    plugins_dir = config.common['UWSGI_PLUGINS_DIR']
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


@uwsgi_manager.command
def debug():
    pidfile = config.common['UWSGI_PIDFILE']
    print('Debugging uWSGI:', end=' ')
    if is_alive(pidfile):
        print(colored('failed', 'red', attrs=['bold']) +
              ', uWSGI is already running.')
    else:
        p = _uwsgi_common(catch_exceptions=True,
                          die_on_term=True, _bg=True)
        print(colored('uWSGI', 'green', attrs=['bold']) + '.')
        try:
            p.wait()
        except KeyboardInterrupt:
            p.terminate()
            p.wait()


@uwsgi_manager.command
def reload():
    pidfile = config.common['UWSGI_PIDFILE']
    print('Reloading uWSGI:', end=' ')
    try:
        uwsgi(reload=pidfile)
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
    else:
        print(colored('uWSGI', 'green', attrs=['bold']) + '.')


@uwsgi_manager.command
def stop():
    pidfile = config.common['UWSGI_PIDFILE']
    print('Stopping uWSGI:', end=' ')
    try:
        uwsgi(stop=pidfile)
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
    else:
        print(colored('uWSGI', 'green', attrs=['bold']) + '.')


@uwsgi_manager.command
def restart():
    pidfile = config.common['UWSGI_PIDFILE']
    stop()
    count = 0
    while is_alive(pidfile):
        print('.', end='')
        count += 1
    print('\b' * count)
    start()


@uwsgi_manager.command
def log():
    uwsgi_logfile = config.common['UWSGI_LOGFILE']
    def process_output(line):
        print(line.strip(), file=sys.stdout)
    p = sh.tail(uwsgi_logfile, follow=True, _out=process_output)
    try:
        p.wait()
    except KeyboardInterrupt:
        print(colored('\nleave log', 'red'))
        p.terminate()
