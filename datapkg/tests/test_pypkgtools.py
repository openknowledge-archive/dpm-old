import os
import shutil

from datapkg.pypkgtools import PyPkgTools
from datapkg.tests.base import TestCase
from datapkg.package import Package

class TestPyPkgTools(TestCase):

    pkg_name = 'testpypkgtools'
    base_path = '/tmp/pypkgtools-testing'
    pkg_path = os.path.join(base_path, pkg_name)

    def setUp(self):
        self.pypkgtools = PyPkgTools()
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)
        self.pkg = Package(self.pkg_name)
        self.pkg.create_file_structure(self.base_path)

    def test_load_distribution(self):
        dist = self.pypkgtools.load_distribution(self.pkg_path)
        assert dist

    def test_read_pkg(self):
        pkg_name = self.pypkgtools.read_pkg_name(self.pkg_path)
        assert pkg_name == self.pkg_name, pkg_name

