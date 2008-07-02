import os
import shutil
import tempfile
import zipfile

import datapkg.package

class TestPackage:

    def setUp(self):
        self.tmp = '/tmp/datapkg-abc'
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        self.install_dir = os.path.join(self.tmp, 'installed')
        os.makedirs(self.install_dir)
        self.pkg_name = 'mytestpkg2'
        self.pkg = datapkg.package.Package(self.pkg_name,
                version='1.0')
        assert self.pkg.name == self.pkg_name

    def tearDown(self):
        pass

    def test_package_attr(self):
        assert self.pkg.name == self.pkg_name

    def test_create_file_structure(self):
        create_dir = os.path.join(self.tmp, 'create-test')
        self.pkg.create_file_structure(create_dir)
        dest = os.path.join(create_dir, self.pkg.name)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy)
        manifest = os.path.join(dest, 'MANIFEST.in')
        assert os.path.exists(manifest)

    def test_install(self):
        create_dir = os.path.join(self.tmp, 'install-test')
        self.pkg.create_file_structure(create_dir)
        pkg_source_path = os.path.join(create_dir, self.pkg.name)
        pkg_pkgs_path = os.path.join(pkg_source_path, self.pkg.name)
        text_fp = os.path.join(pkg_pkgs_path, 'abc.txt')
        fo = open(text_fp, 'w')
        fo.write('testing')
        fo.close()

        self.pkg.install(self.install_dir, pkg_source_path)

        exists = filter(lambda x: x.startswith(self.pkg.name) and x.endswith('.egg'),
                os.listdir(self.install_dir))
        assert len(exists) == 1

        installed_pkg_path = os.path.join(self.install_dir, exists[0])
        installed_pkg_pkgs_path = os.path.join(installed_pkg_path, self.pkg.name)
        installed_text_path =  os.path.join(installed_pkg_pkgs_path, 'abc.txt')
        assert os.path.isdir(installed_pkg_path)
        assert os.path.exists(installed_text_path)


class TestPackageFromDisk:

    @classmethod
    def setup_class(self):
        self.tmp = tempfile.mkdtemp()
        self.tmpdir2 = tempfile.mkdtemp()

        # setup for testing install from a random file
        self.pkg_name = 'mytestpkg2'
        self.filepath = tempfile.mkstemp(suffix='%s-2.1.zip' % self.pkg_name)[1]
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

