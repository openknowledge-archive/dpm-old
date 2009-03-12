import os
import tempfile

import datapkg.index
import datapkg.package

class TestIndex:
    tmpfile = '/tmp/datapkg.db'
    dburi = 'sqlite:///%s' % tmpfile

    def setUp(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)
        self.index = datapkg.index.Index(self.dburi)
        self.index.init()

    def test_db_ok(self):
        assert self.index.dburi is not None
        assert os.path.exists(self.tmpfile)

    def test_list(self):
        pkgs = self.index.list()
        assert len(pkgs) == 0

        pkg = datapkg.package.Package(u'blah')
        self.index.register(pkg)
        pkgs = self.index.list()
        assert len(pkgs) == 1

    def test_has(self):
        pkg_name = u'blah'
        assert not self.index.has(pkg_name)

        pkg = datapkg.package.Package(pkg_name)
        self.index.register(pkg)
        assert self.index.has(pkg_name)

    def test_get(self):
        pkg_name = u'blah'
        pkg = datapkg.package.Package(pkg_name)
        self.index.register(pkg)
        out = self.index.get(pkg_name)
        assert out.name == pkg_name
        assert out.metadata.name == pkg_name

    def test_get_when_loaded_as_new_and_init_not_called(self):
        pkg_name = u'blah'
        pkg = datapkg.package.Package(pkg_name)
        self.index.register(pkg)

        # clear session so we know this is loaded from db
        self.index.session.clear()

        out = self.index.get(pkg_name)
        assert out.name == pkg_name
        print out.metadata.name
        assert out.metadata.name == pkg_name

