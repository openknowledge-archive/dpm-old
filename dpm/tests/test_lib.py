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

class TestLib:
    def test_get_config(self):
        assert lib.get_config() == dpm.CONFIG.sections()
        assert dpm.CONFIG.options('index:ckan') == lib.get_config(section="index:ckan")
        assert dpm.lib.get_config('index:ckan','ckan.url') == 'http://thedatahub.org/api/'

    @raises(ValueError)
    def test_get_config_error(self):
        lib.get_config(None, 'index:ckan')

    def test_set_config(self):
        value = lib.set_config("test:section", "test.option", "testvalue")
        assert value == "testvalue"
        assert lib.get_config("test:section") == ["test.option"]
        #clean up
        dpm.CONFIG.remove_section("test:section")
        dpm.CONFIG.write(open(dpm.config.default_config_path,'w'))

    def test_delete_config(self):
        value = lib.set_config("test:section", "test.option", "testvalue")
        new_value = lib.delete_config("test:section", "test.option")
        assert new_value == ""
        #clean up
        dpm.CONFIG.remove_section("test:section")
        dpm.CONFIG.write(open(dpm.config.default_config_path,'w'))

    def test_index_from_spec(self):
        ckan_idx = lib.index_from_spec(CKAN_SPEC)
        assert type(ckan_idx[0]) == dpm.index.ckan.CkanIndex
        assert ckan_idx[1] == '' #must be an empty string
        ckan_idx = lib.index_from_spec(PACKAGE_SPEC)
        assert type(ckan_idx[0]) == dpm.index.ckan.CkanIndex
        assert ckan_idx[1] == PACKAGE_NAME

    def test_init(self):
        path = tempfile.mkdtemp()
        package_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))
        package = lib.init(path, package_name)
        assert package.name == package_name
        package_path = os.path.join(path, package.name)
        assert os.path.exists(package_path)
        assert os.path.exists(package_path)
        assert os.path.isfile(package_path+os.sep+DATAPACKAGE)

    def test_save(self):
        path = tempfile.mkdtemp()
        package_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))

        inited_package = lib.init(path, package_name)
        inited_package.author = 'John Doe'

        inited_package = lib.save(inited_package)
        assert inited_package.installed_path == os.path.join(path, inited_package.name)
        assert inited_package.author == 'John Doe'
        #extra check
        inited_package = dpm.package.Package.load(os.path.join(path, inited_package.name))
        assert inited_package.author == 'John Doe'

    @raises(ValueError)
    def test_save_error(self):
        path = tempfile.mkdtemp()
        package_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))
        non_inited_package = dpm.package.Package()
        non_inited_package.author = 'John Doe'
        non_inited_package = lib.save(non_inited_package)

    def test_load(self):
        path = tempfile.mkdtemp()
        package_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))

        inited_package = lib.init(path, package_name)
        inited_package.author = 'Jack the Packager'

        inited_package = lib.save(inited_package)

        inited_package = dpm.lib.load(os.path.join(path, inited_package.name))
        assert inited_package.author == 'Jack the Packager'


