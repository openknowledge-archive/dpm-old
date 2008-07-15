import os
import tempfile
import shutil
from StringIO import StringIO

from datapkg.tests.base import TestCase

import datapkg.repository

class TestRepository(TestCase):

    def setUp(self):
        self.make_tmpdir()
        self.init_path = os.path.join(self.tmpdir, '.datapkg')
        self.repo = datapkg.repository.Repository(self.init_path)

    def test_paths(self):
        config_path = os.path.join(self.init_path, 'config.ini')
        assert config_path == self.repo.config_path

    def test_index(self):
        assert self.repo.index_dburi == 'sqlite:///%s' % self.repo.index_path
        assert self.repo.index is not None

    def test_init(self):
        self.repo.init()
        assert os.path.exists(self.repo.config_path)
        assert os.path.exists(self.repo.index_path)
        assert os.path.exists(self.repo.installed_path)

