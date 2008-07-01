import os
import shutil
import tempfile
import zipfile

import datapkg.package

class TestPackagePlain:
 
    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp2 = tempfile.mkstemp(suffix='-2.1.zip')[1]
        zf = zipfile.ZipFile(self.tmp2, 'w')
        self.meta = 'title: xyz'
        zf.writestr('metadata.txt', self.meta)
        zf.writestr('data.csv', '1,3,5')
        zf.close()

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)
        os.remove(self.tmp2)

    def test_package_attr(self):
        pkg = datapkg.package.PackagePlain('mytestpkg', title='jones')
        assert pkg.name == 'mytestpkg'
        assert pkg.title == 'jones'

    def test_package_plain(self):
        pkg = datapkg.package.PackagePlain('mytestpkg')
        pkg.download_url = 'file://%s' % self.tmp2
        # install using external system (if required)
        # and install here
        pkg.install(self.tmp)
        metafo = pkg.resource_stream('metadata.txt')
        meta = metafo.read()
        assert meta == self.meta


class TestPackagePython:

    def test_package_egg(self):
        # how do we test install easily ...

        # datapkg is already installed (by defn) so use that
        pkg = datapkg.package.PackagePython('datapkg')
        fo = pkg.resource_stream('__init__.py')
        out = fo.read()
        assert len(out) > 0
        assert out.startswith("'''datapkg is a tool")

    def test_pkg_resources(self):
        # import pkg_resources
        # pkg_resources
        pass

