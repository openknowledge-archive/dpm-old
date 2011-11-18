import dpm.lib as lib
import tempfile
import os
import random
import string
import dpm
import dpm.index.ckan
import dpm.package
from nose.tools import raises

# A package in CKAN index for testing. It has three resources: two in CKAN storage, one on task3.cc
CKAN_SPEC = 'ckan://'
PACKAGE_NAME = 'datapkg-gui-test'
PACKAGE_SPEC = CKAN_SPEC+PACKAGE_NAME
DATAPACKAGE = 'datapackage.json'
EXPECTED_RESOURCES = ('bugs-long.csv', 'bugs-short.csv', 'output.dat')

class TestLibInternet:
    __external__ = True

    def test_list(self):
        ckan_list = lib.list(CKAN_SPEC)
        assert len(ckan_list) > 2000
        package_names = []
        for package in ckan_list:
            package_names.append(package.name)
        assert PACKAGE_NAME in package_names #datapkg-gui-test is an already imported package

    def test_search(self):
        test_package = lib.search(CKAN_SPEC, PACKAGE_NAME)
        assert len(test_package) > 0
        assert test_package[0].name == PACKAGE_NAME

    def test_info(self):
        manifest, metadata = lib.info(PACKAGE_SPEC)
        assert metadata['name'] == PACKAGE_NAME
        assert len(metadata['resources']) == len(EXPECTED_RESOURCES)
        
    def test_get_package(self):
        package = lib.get_package(PACKAGE_SPEC)
        assert package.name == PACKAGE_NAME
        assert len(package.resources) == len(EXPECTED_RESOURCES)
        
    def test_download(self):
        download_path = tempfile.mkdtemp()
        lib.download(PACKAGE_SPEC, download_path)
        pkg_path = download_path+os.sep+PACKAGE_NAME
        assert os.path.exists(pkg_path)
        assert os.path.isfile(pkg_path+os.sep+DATAPACKAGE)
        for res in EXPECTED_RESOURCES:
            assert os.path.isfile(pkg_path+os.sep+res)

