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
        pkgs = self.index.list_packages()
        assert len(pkgs) == 0

        pkg = datapkg.package.Package('blah')
        self.index.register(pkg)
        pkgs = self.index.list_packages()
        assert len(pkgs) == 1


