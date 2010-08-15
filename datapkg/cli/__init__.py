'''datapkg command line interface.

See datapkg help for details.
'''
import sys
import os
import optparse
import logging
from StringIO import StringIO
import traceback
import time

logger = logging.getLogger('datapkg.cli')
# set this up below
# logging.basicConfig(level=logging.DEBUG)

import datapkg
import datapkg.spec

parser = optparse.OptionParser(
    usage='''%prog COMMAND [OPTIONS]

Use "datapkg help" see a list of commands.''',
    version=datapkg.__version__)

parser.add_option(
    '-v', '--verbose',
    dest='verbose',
    action='count',
    default=0,
    help='Give more output')
parser.add_option(
    '-d', '--debug',
    dest='debug',
    default=False,
    action='store_true',
    help='Print debug output')
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
# TODO: put in defaults for repo and config
import datapkg.config
parser.add_option(
    '-c', '--config',
    dest='config',
    help='Path to config file (if any) - defaults to %s' % datapkg.config.default_config_path)
parser.add_option(
    '-r', '--repository',
    dest='repository',
    help='Path to repository - overrides value in config'
    )
parser.add_option(
    '-k', '--api-key',
    dest='api_key',
    default=None,
    help='CKAN API Key (overrides value in config)')

_commands = {}

class Command(object):
    name = None
    usage = None
    min_args = None
    max_args = None

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

    def merge_options(self, initial_options, options):
        for attr in ['log']:
            setattr(options, attr, getattr(initial_options, attr) or getattr(options, attr))
        options.quiet += initial_options.quiet
        options.verbose += initial_options.verbose

    def index_from_spec(self, spec_str, all_index=False):
        spec = datapkg.spec.Spec.parse_spec(spec_str, all_index=all_index)
        return spec.index_from_spec()

    def _print(self, msg, force=False):
        if self.level >= 1 or force:
            print(msg)

    def _print_pkg(self, pkg):
        print u'## Package: %s' % pkg.name
        print
        out = pkg.pretty_print()
        print out
    
    def _check_args(self, args):
        if self.min_args is not None and len(args) < self.min_args:
            print 'Insufficient arguments. See command help'
            return False
        if self.max_args is not None and len(args) > self.max_args:
            print 'Too many arguments. See command help'
            return False
        return True

    def main(self, complete_args, args, initial_options):
        options = initial_options
        discarded_options, args = self.parser.parse_args(args)
        # From pip but not needed by us I think
        # self.merge_options(initial_options, options)
        self.options = options
        self.verbose = options.verbose
        import datapkg.config
        # datapkg.CONFIG now set
        if options.config:
            datapkg.CONFIG = datapkg.config.load_config(options.config)
        if options.api_key:
            datapkg.CONFIG.set('DEFAULT', 'ckan.api_key', self.options.api_key)
        if options.repository:
            datapkg.CONFIG.set('DEFAULT', 'repo.default_path',
                    options.repository)

        ## set up logging
        if options.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARN)
        # TODO: fix up logger
        level = 1 # Notify
        level += options.verbose
        level -= options.quiet
        self.level = level

        complete_log = []
        if options.log:
            log_fp = open_logfile_append(options.log)
            # TODO: add additional listener ...
            # logger.consumers.append((logger.DEBUG, log_fp))
        else:
            log_fp = None

        exit = 0
        if not self._check_args(args):
            sys.exit(2)
        try:
            self.run(options, args)
        except:
            logger.fatal('Exception:\n%s' % format_exc())
            exit = 2
        
        if log_fp is not None:
            log_fp.close()
        if exit:
            try:
                log_fn = 'datapkg-log.txt'
                text = '\n'.join(complete_log)
                # Not sure we need to tell people ...
                # logger.fatal('Storing complete log in %s' % log_fn)
                log_fp = open_logfile_append(log_fn)
                log_fp.write(text)
                log_fp.close()
            except IOError:
                pass
        sys.exit(exit)


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


class LicenseCommand(Command):
    name = 'license'
    usage = '%prog'
    summary = 'Show the license'

    def run(self, options, args):
        license = datapkg.__license_full__
        print license


class ManCommand(Command):
    name = 'man'
    usage = '%prog'
    summary = 'Show the manual'

    def run(self, options, args):
        info = datapkg.__doc__
        print
        print '                   ## DataPkg Manual ##'
        print '\n' + info


class ListCommand(Command):
    name = 'list'
    summary = 'List registered packages'
    min_args = 0
    max_args = 1
    usage = \
'''%prog [index-spec]

List registered packages. If index-spec is not provided use default index.
'''
    def run(self, options, args):
        if args:
            spec_from = args[0]
        else:
            spec_from = ''
        index, path = self.index_from_spec(spec_from, all_index=True)
        for pkg in index.list():
            print u'%s -- %s' % (pkg.name, pkg.title)


class SearchCommand(Command):
    name = 'search'
    summary = 'Search registered packages'
    min_args = 2
    max_args = 2
    usage = \
'''%prog {index-spec} {query}

Search registered packages in index-spec.
'''
    def run(self, options, args):
        spec_from = args[0]
        query = args[1]
        index, path = self.index_from_spec(spec_from)
        for pkg in index.search(query):
            print u'%s -- %s' % (pkg.name, pkg.title)


class InfoCommand(Command):
    name = 'info'
    summary = 'Get information about a package'
    min_args = 1
    max_args = 2
    usage = \
'''%prog {package-spec} [manifest]

Get information about a package (print package metadata). If manifest specified
then show manifest info rather than package metadata.

WARNING: if you change the metadata for a python distribution you may need to
rebuild the egg-info for changes to show up here.
'''

    def run(self, options, args):
        spec_from = args[0]
        index, path = self.index_from_spec(spec_from)
        pkg = index.get(path)
        if pkg is None:
            print 'No package was found for: "%s"' % spec_from
            return 1
        if len(args) > 1 and args[1] == 'manifest':
            print '### Manifest\n'
            for resource in pkg.manifest:
                print resource
        else:
            self._print_pkg(pkg)


class DumpCommand(Command):
    name = 'dump'
    summary = 'Dump a file from within package'
    min_args = 2
    max_args = 2
    usage = \
'''%prog {pkg-spec} {path-of-resource-within-pkg}

Dump contents of specified resource in specified package to stdout.
'''

    def run(self, options, args):
        spec_from = args[0]
        index, path = self.index_from_spec(spec_from)
        pkg = index.get(path)
        offset = args[1]
        stream = pkg.stream(offset)
        import sys
        sys.stdout.write(stream.read()) 


class InitCommand(Command):
    name = 'init'
    summary = 'Initialise things (config, repository etc)'
    min_args = 1
    max_args = 2
    usage = '''%prog {action}

config [location]: Create configuration file at location. If not location
specified use default (see --config).

index [location]: Initialize an index at location specified in config.

repo: Initialize a repository. The repository will be created at the location
      specified via the --repository option or default location specified by
      config.
'''

    def run(self, options, args):
        action = args[0]
        method = getattr(self, action)
        theirargs = args[1:]
        method(theirargs, options)
    
    def repo(self, args, options):
        import datapkg.repository
        repo = datapkg.repository.Repository(datapkg.CONFIG.get('DEFAULT', 'repo.default_path'))
        repo.init()
        msg = 'Repository successfully initialized at %s' % datapkg.CONFIG.get('DEFAULT', 'repo.default_path')
        self._print(msg)
    
    def config(self, args, options):
        '''Create default config file.'''
        import datapkg.config
        if args:
            cfg = datapkg.config.write_default_config(args[0])
        else:
            cfg = datapkg.config.write_default_config()
    
    def index(self, args, options):
        '''Create default index file.'''
        import datapkg.index
        datapkg.index.get_default_index().init()


class CreateCommand(Command):
    name = 'create'
    summary = 'Create a package'
    min_args = 1
    max_args = 1
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
        import datapkg.distribution
        msg = 'Creating new datapkg: %s' %  path
        self._print(msg)
        datapkg.package.Package.create_on_disk(path)


class RegisterCommand(Command):
    name = 'register'
    summary = 'Register a package'
    min_args = 1
    max_args = 2
    usage = \
'''%prog {src-spec} {dest-spec}

Register package at {src-spec} into index at {dest-spec}.
'''

    def run(self, options, args):
        logger.debug('RegisterCommand: %s (options: %s)' % (args, options))
        spec_from = args[0]
        index, path = self.index_from_spec(spec_from)
        if len(args) == 2:
            spec_to = args[1]
            index_to, path_to = self.index_from_spec(spec_to, all_index=True)
        else:
            logger.debug('RegisterCommand: Loading default index')
            index_to = datapkg.index.get_default_index()
        pkg = index.get(path)
        index_to.register(pkg)


class UpdateCommand(Command):
    name = 'update'
    summary = 'Update a package'
    min_args = 1
    max_args = 2
    usage = \
'''%prog {src-spec} {dest-spec}

As for register.
'''

    def run(self, options, args):
        spec_from = args[0]
        index, path = self.index_from_spec(spec_from)
        if len(args) > 1:
            spec_to = args[1]
            index_to, path_to = self.index_from_spec(spec_to)
        else:
            index_to = datapkg.index.get_default_index()
        pkg = index.get(path)
        index_to.update(pkg)


class InstallCommand(Command):
    name = 'install'
    summary = 'Install a package'
    min_args = 2
    max_args = 2
    usage = \
'''%prog {src-spec} {dest-spec}

Install a package located {src-spec} to {dest-spec}, e.g.::

    install ckan://name path-on-disk
'''

    def run(self, options, args):
        spec_from = args[0]
        spec_to = args[1]
        index, path = self.index_from_spec(spec_from)
        index_to, empty_path = self.index_from_spec(spec_to, all_index=True)
        pkg = index.get(path)
        # TODO: have to reimport here for this to work. Why?
        import datapkg.index
        if not isinstance(index_to, datapkg.index.FileIndex):
            msg = u'You can only install to the local filesystem'
            raise Exception(msg)
        # This is a mess and needs to be sorted out
        # Need to distinguish Distribution from a simple Package and much else

        # TODO: decide what to do with stuff on local filesystem
        # if pkg.installed_path: # on local filesystem ...
        #     import shutil
        #     dest = os.path.join(path_to, pkg.name)
        #     shutil.copytree(pkg.installed_path, dest)

        # go through normal process (may just be metadata right ... not a dist)
        install_path = os.path.join(index_to.index_path, pkg.name)
        # we can assume for present that this is not a real 'package' and
        # therefore first register package on disk
        print 'Registering ... '
        install_path = index_to.register(pkg)
        print 'Created on disk at: %s' % install_path
        resources = set()
        if pkg.resources:
            for resource in resources:
                if resource and isinstance(resource, dict):
                    url = resource.get("url")
                    if url: resources.add(url)
        if pkg.download_url:
            resources.add(pkg.download_url)
        if resources:
            import datapkg.util
            downloader = datapkg.util.Downloader(install_path)
            print 'Downloading package resources ...'
            for url in resources:
                downloader.download(url)
        else:
            msg = u'Warning: no resources to install for package %s (no download url)' % pkg.name
            logger.warn(msg)
            print msg


import pkg_resources
for entry_point in pkg_resources.iter_entry_points('datapkg.cli'):
    cmd = entry_point.load()
    cmdinstance = cmd()
    _commands[cmdinstance.name] = cmdinstance


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

