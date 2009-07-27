from datapkg.tests.base import *
from datapkg.distribution import DistributionBase, PythonDistribution
from datapkg.package import Package


class TestPythonDistribution(TestCase):

    def setUp(self):
        self.make_tmpdir()
        self.tmp = self.tmpdir
        self.install_dir = os.path.join(self.tmp, 'installed')
        os.makedirs(self.install_dir)
        self.pkg_name = 'mytestpkg2'
        self.pkg = Package(self.pkg_name, version='1.0')

    def test_write(self):
        create_dir = os.path.join(self.tmp, 'create-test')
        self.pkg.installed_path = os.path.join(create_dir, self.pkg_name)
        dist = PythonDistribution(self.pkg)
        dist.write()
        dest = os.path.join(create_dir, self.pkg.name)
        setuppy = os.path.join(dest, 'setup.py')
        assert os.path.exists(setuppy), setuppy
        manifest = os.path.join(dest, 'MANIFEST.in')
        assert os.path.exists(manifest)

    def _mock_pkg(self):
        create_dir = os.path.join(self.tmp, 'install-test')
        self.pkg.installed_path = os.path.join(create_dir, self.pkg_name)
        dist = PythonDistribution(self.pkg)
        self.dist = PythonDistribution(self.pkg)
        self.dist.write()
        pkg_source_path = os.path.join(create_dir, self.pkg.name)
        pkg_pkgs_path = os.path.join(pkg_source_path, self.pkg.name)
        text_fp = os.path.join(pkg_pkgs_path, 'abc.txt')
        fo = open(text_fp, 'w')
        fo.write('testing')
        fo.close()
        return pkg_source_path

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


class TestPythonDistributionFromPath(TestCase):

    def setUp(self):
        self.make_tmpdir()
        self.pkg_name = 'abc'
        self.pkg = Package(self.pkg_name,
                version='1.0',
                installed_path=os.path.join(self.tmpdir, self.pkg_name),
                )
        self.dist = PythonDistribution(self.pkg)
        self.dist_path = self.dist.write()

    def test_from_path(self):
        dist = PythonDistribution.from_path(self.dist_path)
        pkg = dist.package
        assert pkg.name == self.pkg_name
        assert pkg.metadata.name == self.pkg_name

