# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


import os
import codecs
import shutil
from termcolor import colored
from jinja2 import Template

from studio.launch import ROOT_PATH
from jinja2 import Environment, FileSystemLoader
JDIR = os.path.join(ROOT_PATH, 'jinja')
JENV = Environment(loader=FileSystemLoader(JDIR))


class cd(object):
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def mkdirs(path):
    try:
        print(colored('create directory %s' % path, 'blue'))
        os.makedirs(path)
    except OSError:
        pass


def writefp(path, text):
    with codecs.open(path, 'wb', 'utf-8') as fp:
        print(colored('create file %s' % path, 'white'))
        fp.write(text)


def build_structure(command, dist='.', tpl='default', **kwargs):
    with cd(dist):
        TEMPLATE_DIR = os.path.join(JDIR, command, tpl)
        for root, dirs, files in os.walk(TEMPLATE_DIR):
            reldir = os.path.relpath(root, start=JDIR)
            relcurdir = os.path.relpath(root, start=TEMPLATE_DIR)
            for dname in dirs:
                dpath = Template(os.path.join(relcurdir,
                                              dname)).render(**kwargs)
                mkdirs(dpath)
            for fname in files:
                real_fname = fname[:-7] if fname.endswith('.jinja2') else fname
                fpath = Template(os.path.join(relcurdir,
                                              real_fname)).render(**kwargs)
                if fname.endswith('.jinja2'):
                    text = JENV.get_template(os.path.join(reldir,
                                                          fname)).render(**kwargs)
                    writefp(fpath, text)
                else:
                    shutil.copyfile(os.path.join(JDIR, reldir, fname), fpath)


if __name__ == '__main__':
    build_structure('pypi', appname='daydayup')
