# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from termcolor import colored
from studio.launch.base import manager
from .contrib import build_structure

app_manager = manager.subcommand('pypi')


@app_manager.command
def init(*appnames):
    print(colored('initializing app ...', 'green'))
    for appname in appnames:
        db_pass = appname[0] * 4
        build_structure('pypi', appname=appname, db_pass=db_pass)
    print(colored('app initializing complete!', 'green'))

