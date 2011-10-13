import os
import shutil
import tempfile
import zipfile

import dpm.package
from dpm.tests.base import TestCase

class TestPackage(TestCase):
    # __test__ = False

    def setUp(self):
        self.make_tmpdir()
        self.tmp = self.tmpdir
        self.install_dir = os.path.join(self.tmp, 'installed')
        os.makedirs(self.install_dir)
        self.pkg_name = 'mytestpkg2'
        self.pkg = dpm.package.Package(name=self.pkg_name, version=u'1.0')
        self.pkg.manifest['data.csv'] = None
        self.pkg.manifest['data.js'] = {'format': 'json'}
        self.installed_path = '/random/path'
        self.pkg.installed_path = self.installed_path

    def test_package_name(self):
        name1 = 'abc3'
        pkg1= dpm.package.Package(name=name1)
        assert pkg1.name == name1, pkg1.name
        return

        # TODO: 2009-07-31 reinstate or remove
        name1 = 'Abc3'
        pkg1= dpm.package.Package(name=name1)
        assert pkg1.name == name1.lower(), pkg1.name

        name1 = 'Abc3-'
        pkg1 = dpm.package.Package(name=name1)
        assert pkg1.name == name1.lower(), name1

        name1 = 'abc:yx'
        ok = False
        try:
            pkg1 = dpm.package.Package(name=name1)
        except:
            ok = True
        assert ok, name1
    
    def test_package_attr(self):
        assert self.pkg.name == self.pkg_name
        assert self.pkg.version == u'1.0'
        # test defaulting
        assert self.pkg.tags == []
        assert self.pkg.extras == {}

    def test_package_metadata(self):
        assert self.pkg.metadata['name'] == self.pkg.name
        assert self.pkg.metadata['version'] == u'1.0'
        assert self.pkg.metadata['title'] == u''

    def test_update_metadata(self):
        self.pkg.update_metadata({'name': 'zzzzzz'})
        assert self.pkg.name == 'zzzzzz'
    
    def test_manifest(self):
        assert len(self.pkg.manifest) == 2
        assert 'data.csv' in self.pkg.manifest
        assert self.pkg.manifest['data.js']['format'] == 'json'
    
    def test_manager_metadata(self):
        assert self.pkg.manager_metadata['installed_path'] == self.installed_path

    def test_info_from_path(self):
        base = os.path.abspath('.')
        name = 'abc'
        path = os.path.join(base, name)
        obase, oname = dpm.package.Package.info_from_path(path)
        assert obase == base
        assert oname == name

    def test_create_on_disk(self):
        self.make_tmpdir()
        self.pkg_name = 'mytestpkg2'
        path = os.path.join(self.tmpdir, self.pkg_name)
        pkg = dpm.package.Package.create_on_disk(path)
        assert os.path.exists(path)
        assert pkg.installed_path == path
        assert pkg.path == path
        assert pkg.manager_metadata['installed_path'] == path

    def test_pretty_print(self):
        out = self.pkg.pretty_print()
        assert out


class TestPackageFromUrlWhenNotAPythonDistribution:
    __test__ = False

    def setUp(self):
        self.tmp_base = '/tmp/dpm-package-TestPackageFormDisk'
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

        self.pkg = dpm.package.Package(self.pkg_name,
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

