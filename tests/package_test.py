import os
import shutil
import tempfile
import zipfile

import datapkg

class TestPackage:
 
    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp2 = tempfile.mkstemp()[1]
        zf = zipfile.ZipFile(self.tmp2, 'w')
        self.meta = 'title: xyz'
        zf.writestr('metadata.txt', self.meta)
        zf.writestr('data.csv', '1,3,5')
        zf.close()

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)
        os.remove(self.tmp2)

    def test_pkg_resources(self):
        # import pkg_resources
        # pkg_resources
        pass

    def test_package_attr(self):
        pkg = datapkg.Package('mytestpkg', title='jones')
        assert pkg.name == 'mytestpkg'
        assert pkg.title == 'jones'

    def test_package_plain(self):
        pkg = datapkg.Package('mytestpkg')
        pkg.download_url = 'file://%s' % self.tmp2
        # install using external system (if required)
        # and install here
        pkg.install(self.tmp)
        metafo = pkg.resource_stream('metadata.txt')
        meta = metafo.read()
        assert meta == self.meta

    def test_package_egg(self):
        # how do we test install easily ...

        # datapkg is already installed (by defn) so use that
        pkg = datapkg.PackagePython('datapkg')
        fo = pkg.resource_stream('__init__.py')
        out = fo.read()
        assert len(out) > 0
        assert out.startswith("'''datapkg is a tool")


