# -*- code: utf-8 -*-
from __future__ import unicode_literals

import os
import imp


class BasicConfig(object):

    def __init__(self, root_path, defaults=None):
#        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def read(self):
        pass


class PyFileConfig(BasicConfig):

    def load(self, filename):
        d = imp.new_module('config')
        d.__file__ = filename
        filename = os.path.join(self.root_path, filename)
        try:
            execfile(filename, d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        rawdict = {}
        for key in dir(d):
            if not key.isupper():
                continue
            rawdict[key] = getattr(d, key)
        return rawdict


if __name__ == '__main__':
    root_path = os.path.split(os.path.realpath(__file__))[0]
    c = PyFileConfig(root_path, defaults={'a': 'aaaa'})
    print c.load('default/development.pycfg')
