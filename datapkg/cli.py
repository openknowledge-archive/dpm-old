import cmd
import sys
import os

class DataPkgAdmin(cmd.Cmd):
    """
    TODO: self.verbose option and associated self._print
    """

    prompt = 'datapkg > '

    def __init__(self):
        cmd.Cmd.__init__(self) # cmd.Cmd is not a new style class

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

    def do_about(self, line=None):
        import datapkg 
        version = datapkg.__version__
        about = \
'''datapkg version %s.

Copyright the Open Knowledge Foundation. datapkg is open-knowledge and
open-source. For license details run the license command.
''' % version
        print about

    def do_license(self, line=None):
        import datapkg 
        license = datapkg.__license_full__
        print license

    def do_quit(self, line=None):
        sys.exit()

    def do_EOF(self, *args):
        print ''
        sys.exit()
    
    # =================
    # Commands

    def do_install(self):
        pass


def main():
    import sys
    adminCmd = DataPkgAdmin()
    if len(sys.argv) < 2:
        adminCmd.run_interactive()
    else:
        args = ' '.join(sys.argv[1:])
        args = args.replace('-','_')
        adminCmd.onecmd(args)

