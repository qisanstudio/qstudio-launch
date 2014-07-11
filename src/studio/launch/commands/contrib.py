# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
from jinja2 import Template
#from launch import ROOT
ROOT = '/home/qisan/workspace/qisanstudio/qstudio-launch/src/studio/launch'
from jinja2 import Environment, FileSystemLoader
JDIR = os.path.join(ROOT, 'jinja')
JENV = Environment(loader=FileSystemLoader(JDIR))


def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def writefp(path, text):
    with open(path, 'wb') as fp:
        fp.write(text)


def build_structure(dist, tpl='default', **kwargs):
    DIST_DIR = os.path.join(ROOT, 'jinja', dist, tpl)
    for root, dirs, files in os.walk(DIST_DIR):
        reldir = os.path.relpath(root, start=JDIR)
        relcurdir = os.path.relpath(root, start=DIST_DIR)
        for dname in dirs:
            dpath = Template(os.path.join(relcurdir, dname)).render(**kwargs)
            mkdirs(dpath)
        for fname in files:
            fpath = Template(os.path.join(relcurdir, fname.rstrip('.jinja2'))).render(**kwargs)
            text = JENV.get_template(os.path.join(reldir, fname)).render()
            writefp(fpath, text)
    print '----------------------'



if __name__ == '__main__':
    build_structure('pypi', appname='daydayup')

