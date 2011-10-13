import os
import tempfile

import dpm.tests.base
import dpm.index
import dpm.index.base
import dpm.package

class TestSimpleIndex(dpm.tests.base.TestCase):
    def setup(self):
        self.index = dpm.index.base.SimpleIndex()

    pkg_title = u'Test Title'
    pkg_id = u'574198fe-4bd1-45d2-bd71-4f97fb4f4b4c'
    # NB: double single quotes ('') do not work yet (str.replace seems too
    # greedy)
    # No indent because python ini files (use in FileIndex) do not preserve
    # leading space and no blank lines for same reason!!
    pkg_notes = '''Monthly gold prices (USD) in London from Bundesbank.
General: Let's put in some quotes "abc", 'abc', "", '.
* Now a bullet point and semi-colon;'''
    pkg_installed_path = '/a/random/path'

    def _make_package(self, pkg_name):
        pkg = dpm.package.Package(name=pkg_name, id=self.pkg_id)
        pkg.title = self.pkg_title
        pkg.notes = self.pkg_notes
        pkg.installed_path = self.pkg_installed_path
        return pkg

    def test_together_has_register_update_list(self):
        pkg_name = u'blah'
        assert not self.index.has(pkg_name)

        pkg = self._make_package(pkg_name)
        self.index.register(pkg)
        assert self.index.has(pkg_name)

        self.index.update(pkg)
        assert self.index.has(pkg_name)

        pkgs = [ pkg for pkg in self.index.list() ]
        assert len(pkgs) == 1

    def test_get(self):
        pkg_name = u'blah'
        pkg = self._make_package(pkg_name)
        self.index.register(pkg)
        out = self.index.get(pkg_name)
        assert out.id == self.pkg_id, out.id
        assert out.name == pkg_name
        assert out.title == self.pkg_title
        print self.pkg_notes
        print out.notes
        assert out.notes == self.pkg_notes, out.notes
    
    def test_search(self):
        pkg_name = u'searchtest'
        pkg = self._make_package(pkg_name)
        self.index.register(pkg)
        pkgs = [ pkg for pkg in self.index.search('search') ]
        assert len(pkgs) == 1
        

class TestFileIndex(TestSimpleIndex):
    def setup(self):
        self.make_tmpdir()
        self.index = dpm.index.base.FileIndex(self.tmpdir)

