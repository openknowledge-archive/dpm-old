import os
import tempfile
import shutil
from StringIO import StringIO

import py.test

import datapkg.repository
# beauty of this is we can combine items across many different systems
# pypi, apt ...

class TestRepository:

    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.init_path = os.path.join(self.tmp, '.datapkg')
        # get default
        # cache path = ~/var/lib/datapkg/default/index.csv
        self.repo = datapkg.repository.Repository(self.init_path)

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)

    def test_paths(self):
        config_path = os.path.join(self.init_path, 'config.ini')
        assert config_path == self.repo.config_path

    def test_index(self):
        assert self.repo.index_dburi == 'sqlite://%s' % self.repo.index_path
        assert self.repo.index is not None

    def test_init(self):
        self.repo.init()
        assert os.path.exists(self.repo.config_path)
        assert os.path.exists(self.repo.index_path)

    def test_install(self):
        # pkg = ...
        # repo.install(pkg)
        pass

