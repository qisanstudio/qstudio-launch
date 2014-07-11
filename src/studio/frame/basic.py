# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
全局配置管理

"""

import os


BASIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config')


def load_file(path=BASIC_CONFIG_PATH, env='development', suffix='pycfg'):

    fn = os.path.join(path, '.'.join([env, suffix]))
    with open(fn, 'rb') as f:
        return f.read()


