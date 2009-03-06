import sys
import os
import optparse
import logging
from StringIO import StringIO
import traceback
import time

logger = logging.getLogger('datapkg.cli')
## FIXME
logging.basicConfig()

import datapkg

parser = optparse.OptionParser(
    usage='%prog COMMAND [OPTIONS]',
    version=datapkg.__version__)

parser.add_option(
    '-v', '--verbose',
    dest='verbose',
    action='count',
    default=0,
    help='Give more output')
parser.add_option(
    '-q', '--quiet',
    dest='quiet',
    action='count',
    default=0,
    help='Give less output')
parser.add_option(
    '--log',
    dest='log',
    metavar='FILENAME',
    help='Log file where a complete (maximum verbosity) record will be kept')
parser.add_option(
    '-r', '--repository',
    dest='repository',
    help='Path to repository (if non-default)',
    default=None)
# TODO: this should be made specific to CreateCommand
parser.add_option(
    '-t', '--template',
    dest='template',
    action='store',
    default='default',
    help='Specify a template to use when creating on disk (default or flat)')

_commands = {}

class Command(object):
    name = None
    usage = None

    def __init__(self):
        assert self.name
        self.parser = optparse.OptionParser(
            usage=self.usage,
            prog='%s %s' % (sys.argv[0], self.name),
            version=parser.version)
        for option in parser.option_list:
            if not option.dest:
                # -h, --version, etc
                continue
            self.parser.add_option(option)
        _commands[self.name] = self

    def merge_options(self, initial_options, options):
        for attr in ['log']:
            setattr(options, attr, getattr(initial_options, attr) or getattr(options, attr))
        options.quiet += initial_options.quiet
        options.verbose += initial_options.verbose

    def _print(self, msg, force=False):
        if self.verbose or force:
            print(msg)

    def _get_repo(self):
        import datapkg.repository
        repo = datapkg.repository.Repository(self.repository_path)
        return repo

    def _register(self, path):
        import datapkg.package
        pkg = datapkg.package.Package.from_path(path)
        repo = self._get_repo()
        repo.index.register(pkg)
        return (repo, pkg)

    def _get_package(self, path_or_name):
        path_or_name = unicode(path_or_name)
        import datapkg.package
        # this is crude
        is_path = os.path.exists(path_or_name)
        if is_path:
            return datapkg.package.Package.from_path(path_or_name)
        else:
            repo = self._get_repo()
            return repo.index.get_package(path_or_name)

    def main(self, complete_args, args, initial_options):
        options, args = self.parser.parse_args(args)
        self.repository_path = options.repository
        self.verbose = options.verbose
        self.merge_options(initial_options, options)

        # TODO: fix up logger
        level = 1 # Notify
        level += options.verbose
        level -= options.quiet
        complete_log = []
        if options.log:
            log_fp = open_logfile_append(options.log)
            logger.consumers.append((logger.DEBUG, log_fp))
        else:
            log_fp = None

        exit = 0
        try:
            self.run(options, args)
        except:
            logger.fatal('Exception:\n%s' % format_exc())
            exit = 2
        
        if log_fp is not None:
            log_fp.close()
        if exit:
            log_fn = 'datapkg-log.txt'
            text = '\n'.join(complete_log)
            logger.fatal('Storing complete log in %s' % log_fn)
            log_fp = open_logfile_append(log_fn)
            log_fp.write(text)
            log_fp.close()
        sys.exit(exit)


class HelpCommand(Command):
    name = 'help'
    usage = '%prog'
    summary = 'Show available commands'
    general_usage = \
'''%prog [options] <command>

For an introduction to datapkg see the manual:

    $ datapkg man

About information (including license details) is available via `datapkg about`
while a full list of commands is provided by `datapkg help`.
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

HelpCommand()

class AboutCommand(Command):
    name = 'about'
    usage = '%prog'
    summary = 'About datapkg'

    def run(self, options, args):
        about = \
'''datapkg version %s.

datapkg is Open Knowledge and Open Source. For copyright and license details
run the 'license' command.

For more information about datapkg and how to use it run the `man` command.
''' % datapkg.__version__
        print about

AboutCommand()


class LicenseCommand(Command):
    name = 'license'
    usage = '%prog'
    summary = 'Show the license'

    def run(self, options, args):
        license = datapkg.__license_full__
        print license

LicenseCommand()


class ManCommand(Command):
    name = 'man'
    usage = '%prog'
    summary = 'Show the manual'

    def run(self, options, args):
        info = datapkg.__doc__
        print
        print '                   ## DataPkg Manual ##'
        print '\n' + info

ManCommand()


class CkanCommand(Command):
    name = 'ckan'
    usage = '''%prog {action}

ckantags: Prints all the tags in use on the CKAN service.

ckanlist: Prints the names of all the packages registered on the CKAN service.

ckanshow name: Prints the registered details of the named package on the CKAN service.

ckanregister [path] [api-key]

Register a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. If a valid api-key is not
provided, changes to the CKAN register will not be allowed. Please use the
ckanupdate command to update the register when the package metadata changes.

ckanupdate [path] [api-key]

Update a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. If a valid api-key is not
provided, changes to the CKAN register will not be allowed. Please use the
ckanupdate command to update the register when the package metadata changes.
'''
    summary = 'Interact with CKAN'

    def run(self, options, args):
        if args:
            action = args[0]
            if len(args) >= 2:
                self.pkgname = args[1]
            # if options.has_option('base_location'):
            #    self.base_location = args[1]
            self.base_location = None
            method = getattr(self, 'do_' + action)
            method()
        else:
            print 'You must supply an action'

    def do_ckantags(self, line=''):
        import datapkg
        msg = 'Listing all tags registered on CKAN... %s' % self.base_location
        self._print(msg)
        datapkg.ckantags(
            base_location=self.base_location,
        )

    def do_ckanlist(self, line=''):
        import datapkg
        msg = 'Listing packages registered on CKAN... %s' % self.base_location
        self._print(msg)
        datapkg.ckanlist(
            base_location=self.base_location,
        )

    def do_ckanshow(self, line):
        args = line.strip().split(' ')
        pkg_name = args[0]
        import datapkg
        msg = 'Showing details for \'%s\' package registered on CKAN... %s' % (pkg_name, self.base_location)
        self._print(msg)
        datapkg.ckanshow(
            pkg_name=pkg_name,
            base_location=self.base_location,
        )

    def do_ckanregister(self, line):
        args = line.strip().split(' ')
        path = args[0]
        if len(args) > 1:
            api_key = args[1]
        else:
            api_key = None
        if len(args) > 2:
            base_location = args[2]
        else:
            base_location = None
        import datapkg
        msg = 'Registering with CKAN the datapkg on path: %s' %  path
        self._print(msg)
        datapkg.ckanregister(
            path=path,
            base_location=self.base_location,
            api_key=api_key,
        )

    def do_ckanupdate(self, line):
        args = line.strip().split(' ')
        path = args[0]
        if len(args) > 1:
            api_key = args[1]
        else:
            api_key = None
        if len(args) > 2:
            base_location = args[2]
        else:
            base_location = None
        import datapkg
        msg = 'Updating datapkg on CKAN: %s' %  path
        self._print(msg)
        datapkg.ckanupdate(
            path=path,
            base_location=self.base_location,
            api_key=api_key,
        )

CkanCommand()


class InitCommand(Command):
    name = 'init'
    usage = '''%prog

Initialize a repository.

The repository will be created at the default location (see help for command) unless an alternative location is specified via the --repository option.
'''
    summary = 'Initialize a repository'

    def run(self, options, args):
        import datapkg.repository
        try:
            repo = datapkg.repository.Repository(self.repository_path)
            repo.init()
        except Exception, inst:
            print inst
        msg = 'Repository successfully initialized at %s' % self.repository_path
        self._print(msg)
    
InitCommand()


class CreateCommand(Command):
    name = 'create'
    summary = 'Create a package'
    usage = \
'''%prog <path-or-name>

Create a skeleton data package at path. Package Name will be taken from
last portion of path. If path simply a name then create in the current
directory.'''

#     def __init__(self):
#         super(CreateCommand, self).__init__()
#         self.parser.add_option(
#             '-t', '--template',
#             dest='template',
#             action='store',
#             default='default',
#             help='Specify template to use (default or flat)')
 
    def run(self, options, args):
        path = args[0]
        import datapkg.package
        template = options.template 
        msg = 'Creating new datapkg: %s' %  path
        self._print(msg)
        datapkg.package.PackageMaker.create_on_disk(path)

CreateCommand()


class RegisterCommand(Command):
    name = 'register'
    summary = 'Register a package'
    usage = \
'''%prog {path}

Register package at path in the in the local index.
'''

    def run(self, options, args):
        path = args[0]
        self._register(path)

RegisterCommand()


class InstallCommand(Command):
    name = 'install'
    summary = 'Install a package'
    usage = \
'''%prog {path}

Install a package located at path on disk.
'''

    def run(self, options, args):
        pkg_path = args[0]
        pkg_path = line.strip()
        # TODO: check whether it is registered already
        # TODO: option of installing an existing registered package
        repo, pkg = self._register(pkg_path)
        install_dir = repo.installed_path
        pkg.install(install_dir, pkg_path)
        # TODO: save package again as e.g. installed path may have changed
        # This should probably be moved down into package object

InstallCommand()


class InfoCommand(Command):
    name = 'info'
    summary = 'Get information about a package'
    usage = \
'''%prog {path-or-pkg-name}

Get information about a package.
'''

    def run(self, options, args):
        pkg_locator = args[0]
        pkg = self._get_package(pkg_locator)
        if pkg is None:
            print 'No package was found for: "%s"' % pkg_locator
            return 1
        from StringIO import StringIO
        out = StringIO()
        pkg.metadata.write_pkg_file(out)
        out.seek(0)
        print u'## Package: %s' % pkg.name
        print
        print out.read()

InfoCommand()


class DumpCommand(Command):
    name = 'dump'
    summary = 'Dump a resource from a package'
    usage = \
'''%prog {path-or-pkg-name} {path-of-resource-with-pkg}

Dump contents of specified resource in specified package to stdout.
'''

    def run(self, options, args):
        # assuming no spaces in the paths!
        pkg_locator = args[0]
        offset = args[1]
        pkg = self._get_package(pkg_locator)
        stream = pkg.stream(offset)
        import sys
        sys.stdout.write(stream.read()) 

DumpCommand()


# def do_inspect(self, line):
    # pkg_locator = line.strip()
    # pkg = self._get_package(pkg_locator)
    # print pkg.distribution.listdir


def format_exc(exc_info=None):
    if exc_info is None:
        exc_info = sys.exc_info()
    out = StringIO()
    traceback.print_exception(*exc_info, **dict(file=out))
    return out.getvalue()

def open_logfile_append(filename):
    """Open the named log file in append mode.

    If the file already exists, a separator will also be printed to
    the file to separate past activity from current activity.
    """
    exists = os.path.exists(filename)
    log_fp = open(filename, 'a')
    if exists:
        print >> log_fp, '-'*60
        print >> log_fp, '%s run on %s' % (sys.argv[0], time.strftime('%c'))
    return log_fp


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

