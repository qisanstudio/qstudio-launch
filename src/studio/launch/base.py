# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from baker import Baker


class ManagerMixins(object):

    def subcommand(self, name, name_sep=None):
        if name_sep is None and hasattr(self, 'name_sep'):
            name_sep = self.name_sep
        else:
            name_sep = '.'
        return SubManagerWrapper(name, self, name_sep)


class SubManagerWrapper(ManagerMixins):

    def __init__(self, name, parent_manager, name_sep='.'):
        self.name = name
        self.parent_manager = parent_manager
        self.name_sep = '.'

    def command(self, fn=None, name=None, *args, **kwargs):
        if fn is None:
            return lambda fn: self.command(fn,
                                           name=name,
                                           *args, **kwargs)
        else:
            name = self.name + self.name_sep + (name or fn.__name__)
            return self.parent_manager.command(fn,
                                               name=name,
                                               *args, **kwargs)


class Manager(ManagerMixins, Baker):

    def command(self, fn=None, *args, **kwargs):
        if fn is None:
            return lambda fn: self.command(fn,
                                           *args, **kwargs)
        else:
            fn.complete_options = kwargs.pop('complete_options', [])
            return super(Manager, self).command(fn,
                                                *args, **kwargs)

    def complete(self, *argv):
        """自动补全"""
        if len(argv) < 1:
            return
        argv = list(argv)
        argv.pop(0)
        argv_len = len(argv)
        subcommand = argv[0] if argv_len else ''
        complete_options = []
        if subcommand in self.commands:
            subcom = self.commands[subcommand]
            subcommand = argv[1] if argv_len > 1 else ''
            if hasattr(subcom.fn, 'complete'):
                subcom.fn.complete(*argv)
                return
            elif hasattr(subcom.fn, 'complete_options'):
                complete_options = subcom.fn.complete_options
        else:
            complete_options = self.commands.iterkeys()

        for key in complete_options:
            if not subcommand or key.startswith(subcommand):
                print key


manager = Manager()


def load():
    # 引入基本命令
    from . import commands  # noqa

    try:
        # 自动引入 studio.launch 作为扩展
        from studio import launch  # noqa
    except ImportError:
        pass
#    # 通过 entry_points studio.manage_commands 引入更多扩展
#    from pkg_resources import iter_entry_points
#    for ep in iter_entry_points('studio.manage_commands'):
#        ep.load()
#

def main():
    from . import commands
    manager.run()

