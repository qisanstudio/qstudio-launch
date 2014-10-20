# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from termcolor import colored
from studio.launch.base import manager
from .contrib import build_structure

pypi_manager = manager.subcommand('pypi')


@pypi_manager.command
def init(appname, tpl='default'):
    print(colored('initializing app ...', 'green'))
    db_pass = appname[0] * 4
    build_structure('pypi', tpl=tpl, appname=appname, db_pass=db_pass)
    print(colored('app initializing complete!', 'green'))

