import os
import tempfile

import datapkg.tests.base
import datapkg.index
import datapkg.package

class TestSimpleIndex(datapkg.tests.base.TestCase):
    def setup(self):
        self.index = datapkg.index.SimpleIndex()

    def test_together_has_register_update_list(self):
        pkg_name = u'blah'
        assert not self.index.has(pkg_name)

        pkg = datapkg.package.Package(name=pkg_name)
        self.index.register(pkg)
        assert self.index.has(pkg_name)

        self.index.update(pkg)
        assert self.index.has(pkg_name)

        pkgs = [ pkg for pkg in self.index.list() ]
        assert len(pkgs) == 1

    def test_get(self):
        pkg_name = u'blah'
        pkg = datapkg.package.Package(name=pkg_name)
        self.index.register(pkg)
        out = self.index.get(pkg_name)
        assert out.name == pkg_name
    
    def test_search(self):
        pkg_name = u'searchtest'
        pkg = datapkg.package.Package(name=pkg_name)
        self.index.register(pkg)
        pkgs = [ pkg for pkg in self.index.search('search') ]
        assert len(pkgs) == 1
        

class TestFileIndex(TestSimpleIndex):
    def setup(self):
        self.make_tmpdir()
        self.index = datapkg.index.FileIndex(self.tmpdir)

