'''datapkg command line interface.

See datapkg help for details.
'''
import os
import sys
import pkg_resources

from base import Command, parser

_commands = {}


## Need this command in here as it uses the list of commands
class HelpCommand(Command):
    name = 'help'
    usage = '%prog'
    summary = 'Show available commands'
    general_usage = \
'''%prog [options] <command>

For an introduction to datapkg see the manual:

    $ datapkg man

About information (including license details) is available via `datapkg about`.
'''
    
    def run(self, options, args):
        if args:
            ## FIXME: handle errors better here
            command = args[0]
            if command not in _commands:
                raise Exception('No command with the name: %s' % command)
            command = _commands[command]
            command.parser.print_help()
            return
        print self.general_usage
        print 'Commands available:'
        commands = list(set(_commands.values()))
        commands.sort(key=lambda x: x.name)
        for command in commands:
            print '  %s: %s' % (command.name, command.summary)


import pkg_resources
for entry_point in pkg_resources.iter_entry_points('datapkg.cli'):
    cmd = entry_point.load()
    cmdinstance = cmd()
    _commands[cmdinstance.name] = cmdinstance


def main(initial_args=None):
    if initial_args is None:
        initial_args = sys.argv[1:]
    options, args = parser.parse_args(initial_args)
    if not args:
        parser.error('You must give a command (use "datapkg help" see a list of commands)')
    command = args[0].lower()
    if command not in _commands:
        parser.error('No command by the name %s %s' % (os.path.basename(sys.argv[0]), command))
    command = _commands[command]
    command.main(initial_args, args[1:], options)

