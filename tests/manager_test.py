import tempfile
import shutil
from StringIO import StringIO

import py.test

from datapkg import PackageManager
# beauty of this is we can combine items across many different systems
# pypi, apt ...

class TestPackageManager:

    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        # get default
        # cache path = ~/var/lib/datapkg/default/index.csv
        self.pkgmgr = PackageManager(self.tmp)

    def teardown_class(self):
        shutil.rmtree(self.tmp)

    def test_1(self):
        index_list = \
'''
file:///tmp/
'''
        index_csv = \
'''
id1,"some title",metadata_url,data
'''
        index_ini = \
'''
[id1]
title: some title
type: datapkg
download_url: xyz

[id2]
title: military spending information
type: apt
download_url: abc
version: 0.1
'''
        pkgmgr = self.pkgmgr
        pkgmgr.update_index(StringIO(index_ini))
        assert len(pkgmgr) == 2
        pkgs = pkgmgr.search('military spending')
        assert len(pkgs) == 1
        pkg = pkgs[0]
        assert pkg.title == 'military spending information'

    def test_install(self):
        # py.test.raises(pkgmgr.install('id3'), )
        # TODO: create proper download url ...
        # self.pkgmgr.install('id2')
        pass


