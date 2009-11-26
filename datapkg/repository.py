import os
import ConfigParser
import logging

import datapkg
import datapkg.index

logger = logging.getLogger('datapkg.repository')


class StubbedRepo(object):
    pass


class FileRepository(object):
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(os.path.expanduser(repo_path))
        self.index = datapkg.index.FileIndex(self.repo_path)
        self.init()

    def init(self):
        if not os.path.exists(self.repo_path):
            logger.info('Initializing repository at %s' % self.repo_path)
            os.makedirs(self.repo_path)
            os.makedirs(self.installed_path)


class DbRepository(object):
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(os.path.expanduser(repo_path))
        self.installed_path = os.path.join(self.repo_path, 'installed')
        self.index_path = os.path.join(self.repo_path, 'index.db')
        self.index_dburi = 'sqlite:///%s' % self.index_path
        self.index = datapkg.index.DbIndex(self.index_dburi)

    def init(self):
        if not os.path.exists(self.repo_path):
            logger.info('Initializing repository at %s' % self.repo_path)
            os.makedirs(self.repo_path)
            self.index.init()
            os.makedirs(self.installed_path)
        else:
            msg = 'init() failed. It looks like you already ' + \
                    'have something at %s' % self.repo_path
            raise ValueError(msg)

