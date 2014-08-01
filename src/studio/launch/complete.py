# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from .base import manager, load

if __name__ == '__main__':
    cline = os.environ.get('COMP_LINE') or os.environ.get('COMMAND_LINE') or ''
    load()
    manager.complete(*cline.split())
