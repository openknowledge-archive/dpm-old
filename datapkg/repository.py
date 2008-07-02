import os
import ConfigParser

import datapkg
class Repository(object):

    def __init__(self, system_path=None):
        if system_path is None:
            system_path = os.path.join(os.path.expanduser('~'), '.datapkg')
        self.system_path = os.path.abspath(os.path.expanduser(system_path))
        self.config_path = os.path.join(self.system_path, 'config.ini')
        self.index_path = os.path.join(self.system_path, 'index')
        self.installed_path = os.path.join(self.system_path, 'installed')
        self.index = None

    def init(self):
        if not os.path.exists(self.system_path):
            os.makedirs(self.system_path)
            cfg = ConfigParser.SafeConfigParser()
            cfg.set('DEFAULT', 'version', datapkg.__version__)
            cfg.write(file(self.config_path, 'w'))
            # just stub it for time being
            fo = open(self.index_path, 'w').write('')
        else:
            msg = 'init() failed. It looks like you have already ' + \
                    'initialised a datapkg repository at %s' % self.system_path
            raise ValueError(msg)

