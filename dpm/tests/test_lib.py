import dpm.lib as lib
import tempfile
import os
import dpm
import dpm.index.ckan

# A package in CKAN index for testing. It has three resources: two in CKAN storage, one on task3.cc
CKAN = 'ckan://'
PACKAGE = 'datapkg-gui-test'
DATAPACKAGE = 'datapackage.json'
EXPECTED_RESOURCES = ('bugs-long.csv', 'bugs-short.csv', 'output.dat')
class TestLib:
    
    def test_list(self):
        ckan_list = lib.list("ckan://")
        assert len(ckan_list) > 2000
        package_names = []
        for package in ckan_list:
            package_names.append(package.name)
        assert PACKAGE in package_names #datapkg-gui-test is an already imported package

    def test_search(self):
        test_package = lib.search("ckan://", PACKAGE)
        assert len(test_package) > 0
        assert test_package[0].name == PACKAGE

    def test_info(self):
        test_package_metadata = lib.info("ckan://"+PACKAGE) #metadata request
        assert test_package_metadata['name'] == PACKAGE
        assert len(test_package_metadata['resources']) == len(EXPECTED_RESOURCES)

    def test_download(self):
        download_path = tempfile.mkdtemp()
        lib.download("ckan://"+PACKAGE, download_path)
        pkg_path = download_path+os.sep+PACKAGE
        assert os.path.exists(pkg_path)
        assert os.path.isfile(pkg_path+os.sep+DATAPACKAGE)
        for res in EXPECTED_RESOURCES:
            assert os.path.isfile(pkg_path+os.sep+res)

    def test_config(self):
        cfg_lib = lib.get_config()
        cfg_dpm = dpm.CONFIG
        assert cfg_lib == cfg_dpm # dpm.CONFIG is already tested in test_config.py

    def test_index_from_spec(self):
        ckan_idx = lib.index_from_spec(CKAN)
        assert type(ckan_idx[0]) == dpm.index.ckan.CkanIndex
        assert ckan_idx[1] == '' #must be an empty string
        
        