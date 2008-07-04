import cmd
import sys
import os

class DataPkgAdmin(cmd.Cmd):

    prompt = 'datapkg > '

    def __init__(self, verbose=False):
        cmd.Cmd.__init__(self) # cmd.Cmd is not a new style class
        self.verbose = verbose

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

For more information about datapkg and how to use it run the `info` command.
''' % version
        print about

    def do_license(self, line=None):
        import datapkg 
        license = datapkg.__license_full__
        print license

    def do_info(self, line=None):
        import datapkg 
        info = datapkg.__doc__
        print
        print '                   ## DataPkg Tutorial ##'
        print '\n' + info

    def help_info(self, line=None):
        print 'More information about datapkg including a tutorial.'

    def do_quit(self, line=None):
        sys.exit()

    def do_EOF(self, *args):
        print ''
        sys.exit()
    
    # =================
    # Commands

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
'''datapkg ckanregister [path]

Register a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. Please use the ckanupdate
command to update the register when the package information changes."
'''
        print usage

    def do_ckanupdate(self, line):
        path = line.strip()
        import datapkg
        msg = 'Updating datapkg on CKAN: %s' %  path
        self._print(msg)
        datapkg.ckanupdate(path=path)

    def help_ckanupdate(self, line=None):
        import datapkg
        usage = \
'''datapkg ckanupdate [path]

Update a package located at path on disk with the CKAN service. If path 
not provided, it defaults to current directory. If the package has not
already been registered, just use the ckanregister option at first.
'''
        print usage

    def do_create(self, line):
        name = line.strip()
        import datapkg
        msg = 'Creating new datapkg: %s' %  name
        self._print(msg)
        datapkg.create(name=name)

    def help_create(self, line=None):
        import datapkg
        usage = \
'''create <name>

Create a skeleton data package named <name> in the current directory.'''
        print usage

    def do_install(self, line):
        pkg_path = line.strip()
        import datapkg
        if not path:
            path = '.'
        # get repository install_dir
        repo = datapkg.repository.Repository()
        install_dir = repo.installed_path
        pkg = datapkg.package.Package()
        pkg.install(install_dir, pkg_path)
    
    def help_install(self, line=None):
        usage = \
'''datapkg install [path]

Install a package located at path on disk. If path not provided default to
current directory.
'''
        print usage


def main():
    import optparse
    usage = \
'''%prog [options] <command>

Run about or help for details.
'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-v', '--verbose', dest='verbose', help='Be verbose',
            action='store_true', default=False) 
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        return 1
    else:
        adminCmd = DataPkgAdmin()
        args = ' '.join(args)
        adminCmd.onecmd(args)

