# -*- code: utf-8 -*-
from __future__ import unicode_literals

import os
import imp


class BasicConfig(dict):
    
    default_config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'default')
    filename = 'development.pycfg'
    
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})
        self.load()


class PyFileConfig(BasicConfig):

    def load(self):
        d = imp.new_module('config')
        d.__file__ = self.filename
        filename = os.path.join(self.default_config_path, self.filename)
        try:
            execfile(filename, d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        for key in dir(d):
            if key.isupper():
                self[key] = getattr(d, key)


if __name__ == '__main__':
    print PyFileConfig()()