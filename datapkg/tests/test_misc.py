import os

import datapkg
from datapkg.tests.base import TestCase

class TestMisc(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.index_path = os.path.join(self.tmpdir, '.datapkg-index')
        self.repo_path = os.path.join(self.tmpdir, '.datapkg-repo')
        self.index_spec = 'file://%s' % self.repo_path
        self.repo_spec = 'file://%s' % self.repo_path
        self.pkg_name = u'mytestpkg'
        self.pkg_path = os.path.join(self.tmpdir, self.pkg_name)
        self.file_spec = u'file://%s' % self.pkg_path

    def test_load_index(self):
        import datapkg.index
        index = datapkg.load_index(self.index_spec, all_index=True)
        assert isinstance(index, datapkg.index.FileIndex)
        assert index.index_path == self.repo_path, (index.index_path,
                self.repo_path)
    
    # TODO: create a proper package here (are we duplicated cli tests?)
    def _test_load_package(self):
        pkg = datapkg.load_package(self.file_spec)



