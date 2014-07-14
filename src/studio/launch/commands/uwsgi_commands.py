# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import sh
from sh import uwsgi
from termcolor import colored
from studio.launch.base import manager
from .contrib import build_structure

app_manager = manager.subcommand('uwsgi')


@app_manager.command
def start():
    print(colored('starting ...', 'yellow'))
    uwsgi()
    print(colored('start uwsgi compelete', 'green'))

