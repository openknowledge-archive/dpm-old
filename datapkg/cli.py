import cmd
import sys
import os

class DataPkgAdmin(cmd.Cmd):

    prompt = 'datapkg > '

    def __init__(self, repository_path=None, verbose=False):
        cmd.Cmd.__init__(self) # cmd.Cmd is not a new style class
        self.repository_path = repository_path
        self.verbose = verbose

    def default(self, line=None):
        # change the 'default' default to return 1
        print '** Unknown syntax: %s' % line
        return 1

    def run_interactive(self, line=None):
        """Run an interactive session.
        """
        print 'Welcome to datapkg interactive mode\n'
        self.do_about()
        print 'Type:  "?" or "help" for help on commands.\n'
        while 1:
            try:
                self.cmdloop()
                break
            except KeyboardInterrupt:
                raise

    def do_help(self, line=None):
        cmd.Cmd.do_help(self, line)

    def _print(self, msg, force=False):
        if self.verbose or force:
            print(msg)

    ## -----------------------------------------------------------
    ## Standard but specific

    def do_about(self, line=None):
        import datapkg 
        version = datapkg.__version__
        about = \
'''datapkg version %s.

datapkg is Open Knowledge and Open Source. For copyright and license details
run the 'license' command.

For more information about datapkg and how to use it run the `man` command.
''' % version
        print about

    def do_license(self, line=None):
        import datapkg 
        license = datapkg.__license_full__
        print license

    def do_man(self, line=None):
        import datapkg 
        info = datapkg.__doc__
        print
        print '                   ## DataPkg Manual ##'
        print '\n' + info

    def help_man(self, line=None):
        print 'More information about datapkg including a tutorial.'

    def do_quit(self, line=None):
        sys.exit()

    def do_EOF(self, *args):
        print ''
        sys.exit()
    
    # =================
    # Commands

    def do_ckantags(self, line):
        args = line.strip().split(' ')
        if len(args) > 0:
            base_location = args[0]
        else:
            base_location = None
        import datapkg
        msg = 'Listing all tags registered on CKAN... %s' % base_location
        self._print(msg)
        datapkg.ckantags(
            base_location=base_location,
        )

    def help_ckantags(self, line=None):
        import datapkg
        usage = \
'''datapkg ckantags 

Prints the all the tags in use on the CKAN service.
'''
        print usage

    def do_ckanlist(self, line):
        args = line.strip().split(' ')
        if len(args) > 0:
            base_location = args[0]
        else:
            base_location = None
        import datapkg
        msg = 'Listing packages registered on CKAN... %s' % base_location
        self._print(msg)
        datapkg.ckanlist(
            base_location=base_location,
        )

    def help_ckanlist(self, line=None):
        import datapkg
        usage = \
'''datapkg ckanlist 

Prints the names of all the packages registered on the CKAN service.
'''
        print usage

    def do_ckanshow(self, line):
        args = line.strip().split(' ')
        pkg_name = args[0]
        if len(args) > 1:
            base_location = args[1]
        else:
            base_location = None
        import datapkg
        msg = 'Showing details for \'%s\' package registered on CKAN... %s' % (pkg_name, base_location)
        self._print(msg)
        datapkg.ckanshow(
            pkg_name=pkg_name,
            base_location=base_location,
        )

    def help_ckanshow(self, line=None):
        import datapkg
        usage = \
'''datapkg ckanshow name 

Prints the registered details of the named package on the CKAN service.
'''
        print usage

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
            base_location=base_location,
            api_key=api_key,
        )

    def help_ckanregister(self, line=None):
        import datapkg
        usage = \
'''datapkg ckanregister [path] [api-key]

Register a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. If a valid api-key is not
provided, changes to the CKAN register will not be allowed. Please use the
ckanupdate command to update the register when the package metadata changes.
'''
        print usage

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
            base_location=base_location,
            api_key=api_key,
        )

    def help_ckanupdate(self, line=None):
        usage = \
'''datapkg ckanupdate [path] [api-key]

Update a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. If a valid api-key is not
provided, changes to the CKAN register will not be allowed. Please use the
ckanupdate command to update the register when the package metadata changes.
'''
        print usage

    def do_init(self, line=None):
        import datapkg.repository
        try:
            repo = datapkg.repository.Repository(self.repository_path)
            repo.init()
        except Exception, inst:
            print inst
        msg = 'Repository successfully initialized at %s' % self.repository_path
        self._print(msg)
    
    def help_init(self, line=None):
        import datapkg.repository
        usage = \
'''init

Initialize a repository.

The repository will be created at the default location:

    %s

Unless an alternative location is specified via the --repository option.
''' % datapkg.repository.Repository.default_path()
        print usage

    def do_create(self, line):
        path = line.strip()
        import datapkg.package
        msg = 'Creating new datapkg: %s' %  path
        self._print(msg)
        datapkg.package.PackageMaker.create_on_disk(path)

    def help_create(self, line=None):
        import datapkg
        usage = \
'''create <path-or-name>

Create a skeleton data package at path. Package Name will be taken from
last portion of path. If path simply a name then create in the current
directory.'''
        print usage

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

    def do_register(self, line):
        path = line.strip()
        self._register(path)

    def help_register(self, line=None):
        usage = \
'''datapkg register {path}

Register package at path in the in the local index.
'''
        print usage

    def do_install(self, line):
        pkg_path = line.strip()
        # TODO: check whether it is registered already
        # TODO: option of installing an existing registered package
        repo, pkg = self._register(pkg_path)
        install_dir = repo.installed_path
        pkg.install(install_dir, pkg_path)
        # TODO: save package again as e.g. installed path may have changed
        # This should probably be moved down into package object
    
    def help_install(self, line=None):
        usage = \
'''datapkg install {path}

Install a package located at path on disk.
'''
        print usage

    def do_info(self, line):
        pkg_locator = line.strip()
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

    def help_info(self, line=None):
        usage = \
'''datapkg info {path-or-pkg-name}

Get information about a package.
'''
        print usage
    
    def do_dump(self, line):
        # assuming no spaces in the paths!
        pkg_locator, offset = line.strip().split()
        pkg = self._get_package(pkg_locator)
        stream = pkg.stream(offset)
        import sys
        sys.stdout.write(stream.read()) 

    def help_dump(self, line=None):
        usage = \
'''datapkg dump {path-or-pkg-name} {path-of-resource-with-pkg}

Dump contents of specified resource in specified package to stdout.
'''
        print usage

    # def do_inspect(self, line):
        # pkg_locator = line.strip()
        # pkg = self._get_package(pkg_locator)
        # print pkg.distribution.listdir


def main():
    import optparse
    import sys
    usage = \
'''%prog [options] <command>

For instructions on using datapkg see the manual by running:

    $ datapkg man

About information (including license details) is available via `datapkg about`
while a full list of commands is provided by `datapkg help`.
'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-v', '--verbose', dest='verbose', help='Be verbose',
            action='store_true', default=False) 
    parser.add_option('-r', '--repository', dest='repository',
        help='Path to repository (if non-default)', default=None)
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        return 1
    else:
        adminCmd = DataPkgAdmin(repository_path=options.repository,
                verbose=options.verbose)
        args = ' '.join(args)
        status = adminCmd.onecmd(args)
        sys.exit(status)

