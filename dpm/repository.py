import os
import ConfigParser
import logging

import dpm

logger = logging.getLogger('dpm.repository')


class StubbedRepo(object):
    pass


class FileRepository(object):
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(os.path.expanduser(repo_path))
        self.index = dpm.index.FileIndex(self.repo_path)
        self.init()

    def init(self):
        if not os.path.exists(self.repo_path):
            logger.info('Initializing repository at %s' % self.repo_path)
            os.makedirs(self.repo_path)
            os.makedirs(self.installed_path)

