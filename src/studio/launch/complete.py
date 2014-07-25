# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from .base import manager

if __name__ == '__main__':
    cline = os.environ.get('COMP_LINE') or os.environ.get('COMMAND_LINE') or ''
    manager.complete(*cline.split())
