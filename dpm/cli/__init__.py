'''dpm command line interface.

See dpm help for details.
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

For an introduction to dpm see the manual:

    $ dpm man

About information (including license details) is available via `dpm about`.
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
        commands = list(set(_commands.keys()))
        commands.sort()
        for command in commands:
            print '  %s: %s' % (command, _commands[command].summary)


import pkg_resources
for entry_point in pkg_resources.iter_entry_points('dpm.cli'):
    cmd = entry_point.load()
    cmdinstance = cmd()
    _commands[entry_point.name] = cmdinstance


def main(initial_args=None):
    if initial_args is None:
        initial_args = sys.argv[1:]
    options, args = parser.parse_args(initial_args)
    if not args:
        parser.error('You must give a command (use "dpm help" see a list of commands)')
    command = args[0].lower()
    if command not in _commands:
        parser.error('No command by the name %s %s' % (os.path.basename(sys.argv[0]), command))
    command = _commands[command]
    command.main(initial_args, args[1:], options)

