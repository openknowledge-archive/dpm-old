import os

from test_base import TestSimpleIndex
import datapkg.index.db


class TestDbIndexSqlite(TestSimpleIndex):
    tmpfile = '/tmp/datapkg.db'
    dburi = 'sqlite:///%s' % tmpfile

    def setup(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)
        self.index = datapkg.index.db.DbIndexSqlite(self.dburi)
        self.index.init()
        
    def test_search(self):
        pass

    def test_manager_metadata(self):
        pkg_name = u'test-manager-metadata'
        pkg = self._make_package(pkg_name)
        self.index.register(pkg)
        out = self.index.get(pkg_name)
        assert out.installed_path == self.pkg_installed_path, out.installed_path
        newpath = '/a/new/path'
        pkg.installed_path = newpath
        self.index.update(pkg)
        out = self.index.get(pkg_name)
        assert out.installed_path == newpath, out.installed_path


class TestDbIndexSqlachemy(TestSimpleIndex):
    __test__ = False

    tmpfile = '/tmp/datapkg.db'
    dburi = 'sqlite:///%s' % tmpfile

    def setup(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)
        self.index = datapkg.index.db.DbIndexSqlalchemy(self.dburi)
        self.index.init()

    def test_db_ok(self):
        assert self.index.dburi is not None
        assert os.path.exists(self.tmpfile)

    def test_list(self):
        pkgs = self.index.list()
        assert len(pkgs.all()) == 0

        pkg = datapkg.package.Package(name=u'blah', id=u'abc')
        self.index.register(pkg)
        pkgs = self.index.list()
        assert len(pkgs.all()) == 1

    def test_get_when_loaded_as_new_and_init_not_called(self):
        pkg_name = u'blah'
        pkg = datapkg.package.Package(name=pkg_name, id=u'abc')
        self.index.register(pkg)

        # clear session so we know this is loaded from db
        self.index.session.clear()

        out = self.index.get(pkg_name)
        assert out.name == pkg_name

