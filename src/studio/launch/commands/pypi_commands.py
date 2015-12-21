# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import string
import random
from termcolor import colored
from studio.launch.base import manager
from .contrib import build_structure

pypi_manager = manager.subcommand('pypi')


def _init_microsite(appname, socket_port, db_pass):
    mail_server = raw_input(colored('input a mail server: ', 'cyan'))
    print(colored('initializing app ...', 'green'))
    alphabet = string.digits + string.ascii_lowercase
    version_num = ''.join(random.sample(alphabet, 12))
    build_structure('pypi',
                    tpl='microsite',
                    appname=appname,
                    db_pass=db_pass,
                    version_num=version_num,
                    socket_port=socket_port,
                    mail_server=mail_server)


def _init_account(appname, socket_port, db_pass):
    mail_server = raw_input(colored('input a mail server: ', 'cyan'))
    admin_nickname = raw_input(colored('input a admin nickname(admin): ', 'cyan'))
    if not admin_nickname:
        admin_nickname = 'admin'
    admin_email = raw_input(colored('input a admin email address: ', 'cyan'))
    admin_password = raw_input(colored('input a admin email password(%s): ' % appname, 'cyan'))
    print(colored('initializing app ...', 'green'))
    db_pass = appname[0] * 4
    alphabet = string.digits + string.ascii_lowercase
    version_num = ''.join(random.sample(alphabet, 12))
    build_structure('pypi',
                    tpl='account',
                    appname=appname,
                    db_pass=db_pass,
                    version_num=version_num,
                    socket_port=socket_port,
                    admin_nickname=admin_nickname,
                    admin_email=admin_email,
                    admin_password=admin_password,
                    mail_server=mail_server)


@pypi_manager.command
def init(appname):
    tpl = raw_input(
        colored('[microsite/account]choice a template(microsite): ', 'cyan'))
    if not tpl:
        tpl = 'microsite'
    socket_port = int(raw_input(
                        colored('input a socket port(eg: 17003): ', 'cyan')))
    db_pass = appname[0] * 4
    if tpl == 'account':
        _init_account(appname, socket_port, db_pass)
    else:
        _init_microsite(appname, socket_port, db_pass)
    print(colored('app initializing complete!', 'green'))
    print(colored('''
    # 创建数据库
    $ sudo su postgres                  # 切到 postgres 用户
    postgres=# createuser {appname} -P   # 新建用户 密码:{db_pass}
    postgres=# createdb {appname} -O{appname}   为{appname} 用户创建数据库

    # 安装应用
    $ cd qsapp-{appname}
    $ npm install       # 手动安装
    $ bower install     # 手动安装
    $ gulp build        # 手动安装
    $ pip install -e .

    # 执行迁移脚本
    $ cd src/{appname}
    $ alembic upgrade head

    # 配置nginx
    $ cdvirtualenv
    $ cd etc/nginx;vim upstreams.conf
    --- upstreams.conf ---
    upstream app_{appname} {{
        server 0.0.0.0:{socket_port};
    }}
    $ cd sites-available;vim site_{appname}.conf
    --- site_{appname}.conf ---
    server {{

    listen 18000;

    server_name dev.{appname}.com;

    location "/" {{
        include uwsgi_params;
        uwsgi_pass app_{appname};
    }}
    }}
    $ cd ../sites-enabled
    $ ln -s ~/.virtualenvs/dev/etc/nginx/sites-available/site_{appname}.conf site_{appname}.conf
        '''.format(appname=appname, db_pass=db_pass, socket_port=socket_port), 'yellow'))
