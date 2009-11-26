import os
import tempfile
import shutil
from StringIO import StringIO

from datapkg.tests.base import TestCase
import datapkg.repository


class _TestFileRepository(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.init_path = os.path.join(self.tmpdir, '.datapkg')

    def test_init(self):
        self.repo = datapkg.repository.FileRepository(self.init_path)
        assert os.path.exists(self.init_path)


class TestDbRepository(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.init_path = os.path.join(self.tmpdir, '.datapkg')
        self.repo = datapkg.repository.DbRepository(self.init_path)

    def test_index(self):
        assert self.repo.index_dburi == 'sqlite:///%s' % self.repo.index_path
        assert self.repo.index is not None

    def test_init(self):
        self.repo.init()
        assert os.path.exists(self.repo.index_path)
        assert os.path.exists(self.repo.installed_path)

