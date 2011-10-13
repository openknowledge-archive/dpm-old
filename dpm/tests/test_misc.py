import os

import dpm
from dpm.tests.base import TestCase

class TestMisc(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.index_path = os.path.join(self.tmpdir, '.dpm-index')
        self.repo_path = os.path.join(self.tmpdir, '.dpm-repo')
        self.index_spec = 'file://%s' % self.repo_path
        self.repo_spec = 'file://%s' % self.repo_path
        self.pkg_name = u'mytestpkg'
        self.pkg_path = os.path.join(self.tmpdir, self.pkg_name)
        self.file_spec = u'file://%s' % self.pkg_path

    def test_load_index(self):
        import dpm.index.base
        index = dpm.load_index(self.index_spec, all_index=True)
        assert isinstance(index, dpm.index.base.FileIndex)
        assert index.index_path == self.repo_path, (index.index_path,
                self.repo_path)
    
    # TODO: create a proper package here (are we duplicated cli tests?)
    def _test_load_package(self):
        pkg = dpm.load_package(self.file_spec)



