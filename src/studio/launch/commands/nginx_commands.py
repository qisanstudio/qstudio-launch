# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
from sh import sudo, ErrorReturnCode
from StringIO import StringIO
from termcolor import colored
from studio.frame import config
from studio.launch.base import manager
from .contrib import mkdirs, build_structure


CONF_DIR = os.path.join(config.common['NGINX_CHROOT'], 'etc/nginx')
nginx_manager = manager.subcommand('nginx')


def _init_nginx():
    mkdirs(CONF_DIR)
    mkdirs(os.path.join(config.common['NGINX_CHROOT'], 'var/lib/nginx/body'))
    mkdirs(os.path.join(config.common['NGINX_CHROOT'], 'var/log/nginx/'))


@nginx_manager.command
def render():
    """
    render 配置
    """
    _init_nginx()
    params = {}
    params['NGINX_CHROOT'] = config.common['NGINX_CHROOT']
    build_structure('nginx', dist=CONF_DIR, **params)
    print(colored('render config complete!', 'green'))
    # TODO ln -s sites-enabled/


@nginx_manager.command
def test():
    """
    测试当前的 nginx 配置是否正确

    """
    print('Testing nginx:', end=' ')
    err = StringIO()
    try:
        sudo.nginx('-p', CONF_DIR, '-c',
                 os.path.join(CONF_DIR, 'nginx.conf'),
                 '-t', _err=err)
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
        print(colored(err.getvalue(), attrs=['bold']), file=sys.stderr)
    else:
        print(colored('success', 'green', attrs=['bold']) + '.')


@nginx_manager.command
def start():
    """
    启动 nginx 进程

    """
    print('Starting nginx:', end=' ')
    err = StringIO()
    print(CONF_DIR)
    try:
        sudo.nginx('-p', CONF_DIR, '-c',
                 os.path.join(CONF_DIR, 'nginx.conf'),
                 _err=err)
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
        print(colored(err.getvalue(), attrs=['bold']), file=sys.stderr)
    else:
        print(colored('nginx', 'green', attrs=['bold']) + '.')


@nginx_manager.command
def stop():
    """
    启动 nginx 进程

    """
    print('Stopping nginx:', end=' ')
    try:
        sudo.nginx('-p', CONF_DIR, '-c',
                 os.path.join(CONF_DIR, 'nginx.conf'),
                 '-s', 'stop')
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
    else:
        print(colored('nginx', 'green', attrs=['bold']) + '.')


@nginx_manager.command
def reload():
    """
    平滑加载 nginx 的配置

    """
    print('Reloading nginx:', end=' ')
    err = StringIO()
    try:
        sudo.nginx('-p', CONF_DIR, '-c',
                 os.path.join(CONF_DIR, 'nginx.conf'),
                 '-s', 'reload', _err=err)
    except ErrorReturnCode:
        print(colored('failed', 'red', attrs=['bold']) + '.')
        print(colored(err.getvalue(), attrs=['bold']), file=sys.stderr)
    else:
        print(colored('nginx', 'green', attrs=['bold']) + '.')


@nginx_manager.command
def restart():
    print('Restarting nginx:', end=' ')
    try:
        sudo.nginx('-p', CONF_DIR, '-c',
                 os.path.join(CONF_DIR, 'nginx.conf'),
                 '-s', 'stop')
    except ErrorReturnCode:
        pass  # ignore
    finally:
        try:
            sudo.nginx('-p', CONF_DIR, '-c',
                     os.path.join(CONF_DIR, 'nginx.conf'))
        except ErrorReturnCode:
            print(colored('failed', 'red', attrs=['bold']) + '.')
        else:
            print(colored('nginx', 'green', attrs=['bold']) + '.')
