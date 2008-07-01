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


class TestPackageFull:

    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.tmpdir2 = tempfile.mkdtemp()

        self.name = 'mytestpkg2'
        self.filepath = tempfile.mkstemp(suffix='%s-2.1.zip' % self.name)[1]
        self.url = 'file://%s' % self.filepath
        zf = zipfile.ZipFile(self.filepath, 'w')
        self.meta = 'title: xyz'
        zf.writestr('metadata.txt', self.meta)
        zf.writestr('data.csv', '1,3,5')
        zf.close()

        self.pkg = datapkg.package.PackageFull(self.name,
                version='1.0',
                download_url=self.url)
        assert self.pkg.name == self.name

    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmp)
        shutil.rmtree(self.tmpdir2)
        os.remove(self.filepath)

    def test_download(self):
        self.pkg.download(self.tmp)
        fn = os.path.basename(self.url)
        assert fn in os.listdir(self.tmp)

    def test_is_python_package(self):
        assert not self.pkg.is_python_package(self.filepath)

    def test_unpack_and_make_python(self):
        outpath = self.pkg.unpack(self.filepath, self.tmpdir2)
        assert outpath == self.tmpdir2
        assert os.path.exists(self.tmpdir2)
        print os.listdir(self.tmpdir2)
        assert len(os.listdir(self.tmpdir2)) > 0

        self.pkg.make_into_python_package(self.tmpdir2)
        setuppy = os.path.join(self.tmpdir2, 'setup.py')
        assert os.path.exists(setuppy)
        # TODO: test contents

    def test_install(self):
        install_dir = self.tmp
        self.pkg.install(install_dir)
        print os.listdir(install_dir)
        exists = filter(lambda x: x.startswith(self.pkg.name) and x.endswith('.egg'),
                os.listdir(install_dir))
        assert len(exists) == 1
        # TODO: check contents
        # for some reason cannot access this dir
        # fp = exists[0]
        # fo = file(fp)
        # print fo.read()

    # def test_download_svn(self):
    #    pass

    # def test_make_into_python_package(self):
    #    pass


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

