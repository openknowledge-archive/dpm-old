'''dpm command line interface.

See dpm help for details.
'''
import sys
import logging

logger = logging.getLogger('dpm.cli')
# set this up below
# logging.basicConfig(level=logging.DEBUG)

import dpm
import dpm.spec
from dpm.cli.base import Command


class AboutCommand(Command):
    name = 'about'
    usage = '%prog'
    summary = 'About dpm'

    def run(self, options, args):
        about = \
'''dpm version %s.

dpm is Open Knowledge and Open Source. For copyright and license details
run the 'license' command.

For more information about dpm and how to use it run the `man` command.
''' % dpm.__version__
        print about


class LicenseCommand(Command):
    name = 'license'
    usage = '%prog'
    summary = 'Show the license'

    def run(self, options, args):
        license = dpm.__license_full__
        print license


class ManCommand(Command):
    name = 'man'
    usage = '%prog'
    summary = 'Show the manual'

    def run(self, options, args):
        info = dpm.__doc__
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
        sys.stdout.write(stream.read()) 


class SetupCommand(Command):
    name = 'setup'
    summary = 'Setup things (config, repository etc)'
    min_args = 1
    max_args = 2
    usage = '''%prog {action}

config [location]: Create configuration file at location. If not location
specified use default (see --config).

index [location]: Setup an index at location specified in config.

repo: Setup a repository. The repository will be created at the location
      specified via the --repository option or default location specified by
      config.
'''

    def run(self, options, args):
        action = args[0]
        method = getattr(self, action)
        theirargs = args[1:]
        method(theirargs, options)
    
    def repo(self, args, options):
        import dpm.repository
        repo = dpm.repository.Repository(dpm.CONFIG.get('dpm', 'repo.default_path'))
        repo.init()
        msg = 'Repository successfully setup at %s' % dpm.CONFIG.get('dpm', 'repo.default_path')
        self._print(msg)
    
    def config(self, args, options):
        '''Create default config file.'''
        import dpm.config
        if args:
            cfg = dpm.config.write_default_config(args[0])
        else:
            cfg = dpm.config.write_default_config()
    
    def index(self, args, options):
        '''Create default index file.'''
        import dpm.index
        dpm.index.get_default_index().init()


class InitCommand(Command):
    name = 'init'
    summary = 'Initialize a data package'
    min_args = 1
    max_args = 1
    usage = \
'''%prog <path-or-name>

Initialize a data package at path. Package Name will be taken from
last portion of path. If path simply a name then create in the current
directory.'''

    def run(self, options, args):
        import dpm.package
        path = args[0]
        dpm.package.Package.create_on_disk(path)
        msg = 'Initialized data package on disk at: %s' % path
        self.logger.info(msg)
        self._print(msg)


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
            index_to = dpm.index.get_default_index()
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
            index_to = dpm.index.get_default_index()
        pkg = index.get(path)
        index_to.update(pkg)

