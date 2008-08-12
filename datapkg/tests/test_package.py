import os
import shutil
import tempfile
import zipfile

import datapkg.package
from datapkg.tests.base import TestCase

class TestPackageMaker(TestCase):
    # __test__ = False

    maker = datapkg.package.PackageMaker()

    def test_info_from_path(self):
        base = os.path.abspath('.')
        name = 'abc'
        path = os.path.join(base, name)
        obase, oname = self.maker.info_from_path(path)
        assert obase == base
        assert oname == name

    def test_create_on_disk(self):
        self.make_tmpdir()
        self.pkg_name = 'mytestpkg2'
        path = os.path.join(self.tmpdir, self.pkg_name)
        pkg = self.maker.create_on_disk(path)
        assert os.path.exists(path)


class TestPackage(TestCase):
    # __test__ = False

    def setUp(self):
        self.make_tmpdir()
        self.tmp = self.tmpdir
        self.install_dir = os.path.join(self.tmp, 'installed')
        os.makedirs(self.install_dir)
        self.pkg_name = 'mytestpkg2'
        self.pkg = datapkg.package.Package(self.pkg_name, version='1.0')

    def test_package_name(self):
        name1 = 'Abc3'
        pkg1= datapkg.package.Package(name1)
        assert pkg1.name == name1.lower()

        name1 = 'Abc3-'
        pkg1 = datapkg.package.Package(name1)
        assert pkg1.name == name1.lower(), name1

        name1 = 'abc:yx'
        ok = False
        try:
            pkg1 = datapkg.package.Package(name1)
        except:
            ok = True
        assert ok, name1

    def test_package_attr(self):
        assert self.pkg.name == self.pkg_name
        assert self.pkg.metadata.name == self.pkg.name

    def test_create_file_structure(self):
        create_dir = os.path.join(self.tmp, 'create-test')
        self.pkg.create_file_structure(create_dir)
        dest = os.path.join(create_dir, self.pkg.name)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy)
        manifest = os.path.join(dest, 'MANIFEST.in')
        assert os.path.exists(manifest)

    def _mock_pkg(self):
        create_dir = os.path.join(self.tmp, 'install-test')
        self.pkg.create_file_structure(create_dir)
        pkg_source_path = os.path.join(create_dir, self.pkg.name)
        pkg_pkgs_path = os.path.join(pkg_source_path, self.pkg.name)
        text_fp = os.path.join(pkg_pkgs_path, 'abc.txt')
        fo = open(text_fp, 'w')
        fo.write('testing')
        fo.close()
        return pkg_source_path

    def test_install(self):
        pkg_source_path = self._mock_pkg()

        self.pkg.install(self.install_dir, pkg_source_path)
            
        in_install_dir = os.listdir(self.install_dir)
        exists = filter(
            lambda x: x.startswith(self.pkg.name) and x.endswith('.egg'),
            in_install_dir
            )
        assert len(exists) == 1, in_install_dir

        installed_pkg_path = os.path.join(self.install_dir, exists[0])
        installed_pkg_pkgs_path = os.path.join(installed_pkg_path, self.pkg.name)
        installed_text_path =  os.path.join(installed_pkg_pkgs_path, 'abc.txt')
        assert os.path.isdir(installed_pkg_path)
        assert os.path.exists(installed_text_path)

        self._test_stream()

    def _test_stream(self):
        # running this after test_install is not working :(
        # not clear why so run from test_install for time being

        # pkg_source_path = self._mock_pkg()
        # self.pkg.install(self.install_dir, pkg_source_path)

        # fo = self.pkg.stream('abc.txt', install_dir=self.install_dir)
        fo = self.pkg.stream('abc.txt')
        out = fo.read()
        assert out == 'testing'


class TestPackageFromPath(TestCase):
    __test__ = False

    def setUp(self):
        self.make_tmpdir()
        self.pkg_name = 'abc'
        self.pkg = datapkg.package.Package(self.pkg_name,
                version='1.0')
        self.pkg_path = self.pkg.create_file_structure(self.tmpdir)

    def test_from_path(self):
        pkg = datapkg.package.Package.from_path(self.pkg_path)
        assert pkg.name == self.pkg_name
        assert pkg.metadata.name == self.pkg_name


class TestPackageFromUrlWhenNotAPythonDistribution:
    __test__ = False

    def setUp(self):
        self.tmp_base = '/tmp/datapkg-package-TestPackageFormDisk'
        if os.path.exists(self.tmp_base):
            shutil.rmtree(self.tmp_base)
        self.tmpdir = os.path.join(self.tmp_base, 'tmp1')
        self.tmpdir2 = os.path.join(self.tmp_base, 'tmp2')
        self.tmpdir3 = os.path.join(self.tmp_base, 'tmp2')
        os.makedirs(self.tmpdir)
        os.makedirs(self.tmpdir2)

        # setup for testing install from a random file
        self.pkg_name = 'mytestpkg2'
        self.filepath = os.path.join(self.tmp_base, '%s-2.1.zip' % self.pkg_name)
        self.url = 'file://%s' % self.filepath
        zf = zipfile.ZipFile(self.filepath, 'w')
        self.meta = 'title: xyz'
        zf.writestr('metadata.txt', self.meta)
        zf.writestr('data.csv', '1,3,5')
        zf.close()

        self.pkg = datapkg.package.Package(self.pkg_name,
                version='1.0',
                download_url=self.url)
        assert self.pkg.name == self.pkg_name

    def test_download(self):
        self.pkg.download(self.tmpdir)
        fn = os.path.basename(self.url)
        assert fn in os.listdir(self.tmpdir)

    def test_is_python_package(self):
        assert not self.pkg.is_python_package(self.filepath)

    def test_unpack_and_make_python(self):
        outpath = self.pkg.unpack(self.filepath, self.tmpdir)
        assert outpath == self.tmpdir
        assert os.path.exists(self.tmpdir)
        print os.listdir(self.tmpdir)
        assert len(os.listdir(self.tmpdir)) > 0

        dest = self.pkg.make_python_distribution(self.tmpdir2, outpath)
        pypkg_dir = os.path.join(dest, self.pkg_name)
        datacsv_path = os.path.join(pypkg_dir, 'data.csv')
        assert os.path.exists(pypkg_dir)
        assert os.path.exists(datacsv_path)

    def test_install(self):
        install_dir = self.tmpdir
        self.pkg.install(install_dir, zip_safe=False)
        print os.listdir(install_dir)
        exists = filter(lambda x: x.startswith(self.pkg.name) and x.endswith('.egg'),
                os.listdir(install_dir))
        assert len(exists) == 1
        # TODO: check contents
        # for some reason cannot access this dir
        pkg_path = os.path.join(install_dir, exists[0])
        # egg/pkg-name/data.csv
        data_csv_path = os.path.join(pkg_path, self.pkg_name, 'data.csv')
        print data_csv_path
        assert os.path.exists(data_csv_path)
        # print fo.read()

