import os
import ConfigParser

import datapkg
import datapkg.index


class Repository(object):

    @classmethod
    def default_path(cls):
        return os.path.join(os.path.expanduser('~'), '.datapkg')

    def __init__(self, repo_path=None):
        if repo_path is None:
            repo_path = self.default_path()
        self.repo_path = os.path.abspath(os.path.expanduser(repo_path))
        self.config_path = os.path.join(self.repo_path, 'config.ini')
        self.installed_path = os.path.join(self.repo_path, 'installed')
        self.index_path = os.path.join(self.repo_path, 'index.db')
        self.index_dburi = 'sqlite:///%s' % self.index_path
        self.index = datapkg.index.Index(self.index_dburi)

    def _make_default_config(self, path):
        cfg = ConfigParser.SafeConfigParser()
        cfg.set('DEFAULT', 'version', datapkg.__version__)
        cfg.write(file(path, 'w'))

    def init(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            self._make_default_config(self.config_path)
            self.index.init()
            os.makedirs(self.installed_path)
        else:
            msg = 'init() failed. It looks like you already ' + \
                    'have something at %s' % self.repo_path
            raise ValueError(msg)

