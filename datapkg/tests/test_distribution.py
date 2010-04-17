from datapkg.tests.base import *
from datapkg.distribution import DistributionBase, PythonDistribution, IniBasedDistribution
from datapkg.package import Package


class TestPythonDistribution(TestCase):

    def setUp(self):
        self.make_tmpdir()
        self.install_dir = os.path.join(self.tmpdir, 'installed')
        os.makedirs(self.install_dir)
        self.pkg_name = 'mytestpkg2'
        self.pkg = Package(name=self.pkg_name, version='1.0')

    # do not include in setUp as uses write which we need to test
    def _mock_pkg(self):
        create_dir = os.path.join(self.tmpdir, 'install-test')
        dest_path = os.path.join(create_dir, self.pkg_name)
        dist = PythonDistribution(self.pkg)
        self.dist = PythonDistribution(self.pkg)
        self.dist.write(dest_path)
        pkg_source_path = os.path.join(create_dir, self.pkg.name)
        pkg_pkgs_path = os.path.join(pkg_source_path, self.pkg.name)
        text_fp = os.path.join(pkg_pkgs_path, 'abc.txt')
        fo = open(text_fp, 'w')
        fo.write('testing')
        fo.close()
        # need to rebuild the egg_info at this point or abc.txt not picked up
        # TODO: this is really non-optimal
        current_dir = os.getcwd()
        os.chdir(pkg_source_path)
        os.system('python setup.py -q egg_info')
        os.chdir(current_dir)
        return pkg_source_path

    def test_write(self):
        create_dir = os.path.join(self.tmpdir, 'create-test')
        dest_path = os.path.join(create_dir, self.pkg_name)
        print dest_path
        dist = PythonDistribution(self.pkg)
        dist.write(dest_path)
        dest = os.path.join(create_dir, self.pkg.name)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy), setuppy
        manifest = os.path.join(dest, 'MANIFEST.in')
        assert os.path.exists(manifest)

    def test_install(self):
        pkg_source_path = self._mock_pkg()

        self.dist.install(self.install_dir, pkg_source_path)
            
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
        fo = self.dist.stream('abc.txt')
        out = fo.read()
        assert out == 'testing'

#
#    def setUp(self):
#        self.make_tmpdir()
#        self.pkg_name = 'abc'
#        self.pkg = Package(name=self.pkg_name,
#                version='1.0',
#                installed_path=os.path.join(self.tmpdir, self.pkg_name),
#                )
#        self.dist = PythonDistribution(self.pkg)
#        self.dist_path = self.dist.write()

    def test_load(self):
        pkg_path = self._mock_pkg()
        dist = PythonDistribution.load(pkg_path)
        pkg = dist.package
        assert pkg.name == self.pkg_name
        assert pkg.installed_path == pkg_path
        # at the present write (used in _mock_pkg) does not use pkg metadata!
        # assert pkg.version == '1.0', pkg
        assert pkg.version == '0.1', pkg
        print pkg_path
        assert 'mytestpkg2/abc.txt' in pkg.manifest, pkg.manifest


class TestIniBasedDistribution:
    @classmethod
    def setup_class(self):
        self.tmpDir = tempfile.mkdtemp()
        self.title = 'annakarenina'
        self.dist_path = os.path.join(self.tmpDir, self.title)
    
    @classmethod
    def teardown_class(self):
        shutil.rmtree(self.tmpDir)

    @classmethod
    def _make_test_data(self, basePath, title):
        full_meta = \
'''[DEFAULT]
id : %s
title: %s
creator: abc
description: a long description
comments: here are some additional comments
requires-compilation: y

[manifest::data.csv]
title: my csv file

[manifest::xyz.png]
title: my graph
'''
        os.makedirs(basePath)
        ff = file(os.path.join(basePath, 'metadata.txt'), 'w')
        metadata = full_meta % (title, title)
        ff.write(metadata)
        ff.close()

    def test_load(self):
        self._make_test_data(self.dist_path, self.title)
        dist = IniBasedDistribution.load(self.dist_path)
        pkg = dist.package
        assert pkg.name == self.title, pkg
        assert pkg.title == self.title
        assert u'a long description' in pkg.notes
        assert u'additional comment' in pkg.notes
        assert pkg.author == u'abc'
        assert pkg.extras['requires-compilation'] == 'y'
        # test manifest
        assert len(pkg.manifest) == 2
        assert pkg.manifest['data.csv']['title'] == 'my csv file'
    
    def test_write(self):
        name = 'abc'
        destpath = os.path.join(self.tmpDir, name)
        pkg = Package(name='abc')
        # have % and unicode values
        pkg.title = u'\xa3 1000 %'
        pkg.manifest['data.csv'] = {'price': u'\xa3 1000'}
        dist = IniBasedDistribution(pkg)
        dist.write(destpath)
        metapath = os.path.join(destpath, 'metadata.txt')
        assert os.path.exists(destpath)
        assert os.path.exists(metapath)
        meta = file(metapath).read()
        assert '[DEFAULT]' in meta, meta
        assert 'name = abc' in meta, meta
        assert u'title = \xa3 1000'.encode('utf8') in meta, meta
        assert '[manifest::data.csv]' in meta, meta

