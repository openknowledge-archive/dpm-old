'''dpm command line interface.

See dpm help for details.
'''
import sys
import os
import optparse
import logging
from StringIO import StringIO
import traceback
import time

logger = logging.getLogger('dpm.cli')
# set this up below
# logging.basicConfig(level=logging.DEBUG)

import dpm
import dpm.spec

parser = optparse.OptionParser(
    usage='''%prog COMMAND [OPTIONS]

Use "help" command to see a list of commands.''',
    version=dpm.__version__)

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
import dpm.config
parser.add_option(
    '-c', '--config',
    dest='config',
    help='Path to config file (if any) - defaults to %s' % dpm.config.default_config_path)
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


class Command(object):
    '''Base command class that all dpm Commands should inherit from.
    
    An inheriting class should provide a `run` method and can define the
    following class level attributes (documented below):

    * name
    * summary
    * usage
    * min_args
    * max_args
    '''
    #: The name of the command as used on the command line and in help
    name = None
    #: one line summary of this command (used in printing help)
    summary = None
    #: A multiline detailed description of the command
    usage = None
    #: Minimum number of args to the command (not used if set to None)
    min_args = None
    #: Maximum number of args to the command (not used if set to None)
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
        self.logger = logger

    def merge_options(self, initial_options, options):
        for attr in ['log']:
            setattr(options, attr, getattr(initial_options, attr) or getattr(options, attr))
        options.quiet += initial_options.quiet
        options.verbose += initial_options.verbose

    def index_from_spec(self, spec_str, all_index=False):
        spec = dpm.spec.Spec.parse_spec(spec_str, all_index=all_index)
        return spec.index_from_spec()

    def _print(self, msg, force=False):
        if self.level >= 1 or force:
            print(msg)

    def _print_pkg(self, pkg):
        print u'## Package: %s' % pkg.name
        print
        out = pkg.pretty_print()
        print out.encode("utf-8") ## should really chech the users terminal capability
    
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
        import dpm.config
        # dpm.CONFIG now set
        if options.config:
            dpm.CONFIG = dpm.config.load_config(options.config)
        if options.api_key:
            dpm.CONFIG.set('index:ckan', 'ckan.api_key', self.options.api_key)
        if options.repository:
            dpm.CONFIG.set('dpm', 'repo.default_path',
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
        except Exception, inst:
            print 'Error: %s\n' % inst
            print '[** For (lots) more information run with --debug **]'
            logger.debug('Exception:\n%s' % format_exc())
            exit = 2
        
        if log_fp is not None:
            log_fp.close()
        if exit:
            try:
                log_dir = os.path.expanduser('~/.dpm')
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                log_fn = os.path.join(log_dir, 'dpm-log.txt')
                text = '\n'.join(complete_log)
                # Not sure we need to tell people ...
                # logger.fatal('Storing complete log in %s' % log_fn)
                log_fp = open_logfile_append(log_fn)
                log_fp.write(text)
                log_fp.close()
            except IOError:
                pass
        sys.exit(exit)
    
    def run(self, options, args):
        '''This is the method inheriting classes should override to implement
        their command functionality.

        Inheriting classes should *not* call super to this method -- they
        should just override it.

        :param options: the comand line options (as extracted by optparse).
        :param args: the remaining args (so *not* including the command name).
        '''
        raise NotImplementedError


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


