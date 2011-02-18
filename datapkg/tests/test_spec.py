from datapkg.tests.base import TestCase
from datapkg.spec import *


class TestSpec(TestCase):
    @classmethod
    def setup_class(self):
        self.make_tmpdir()
        self.index_path = os.path.join(self.tmpdir, '.datapkg-index')
        self.repo_path = os.path.join(self.tmpdir, '.datapkg-repo')
        self.index_spec = 'file://%s' % self.repo_path
        self.repo_spec = 'file://%s' % self.repo_path
        self.pkg_name = u'mytestpkg'
        self.pkg_path = os.path.join(self.tmpdir, self.pkg_name)
        self.file_spec = u'file://%s' % self.pkg_path

    def test_01_parse_spec_file_1_bare(self):
        cwd = os.getcwd()
        spec = Spec.parse_spec('file://')
        assert spec.scheme == 'file'
        assert spec.netloc == os.path.dirname(cwd), spec
        assert spec.path == os.path.basename(cwd), spec

    def test_01_parse_spec_file_2_relative_dot(self):
        path = os.getcwd()
        spec = Spec.parse_spec('file://.')
        assert spec.scheme == 'file'
        assert spec.netloc == os.path.dirname(path), spec
        assert spec.path == os.path.basename(path), spec.path

    def test_01_parse_spec_file_2b_relative(self):
        path = os.getcwd()
        spec = Spec.parse_spec('file://jones/abc')
        assert spec.scheme == 'file'
        expnetloc = os.path.join(path, 'jones')
        assert spec.netloc == expnetloc, (expnetloc, spec.netloc)
        assert spec.path == 'abc', spec.path

    def test_01_parse_spec_file_3(self):
        spec = Spec.parse_spec(self.index_spec)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.path == os.path.basename(self.repo_path)

    def test_01_parse_spec_file_4(self):
        spec = Spec.parse_spec(self.repo_spec)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.path == os.path.basename(self.repo_path)

    def test_01_parse_spec_file_5_all_index(self):
        spec = Spec.parse_spec(self.repo_spec, all_index=True)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.netloc == self.repo_path
        assert spec.path == ''

    def test_01_parse_spec_file_6_html_encoding(self):
        spec = Spec.parse_spec('file:///xy%20z/abc')
        assert spec.scheme == 'file', spec.scheme
        assert spec.netloc == '/xy z', spec.netloc
        assert spec.path == 'abc', spec.path

    def test_02_parse_spec_ckan_1(self):
        spec = Spec.parse_spec('ckan:datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.path == 'datapkgdemo', spec.path

    def test_02_parse_spec_ckan_2(self):
        spec = Spec.parse_spec('ckan://datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.netloc == '', spec.netloc 
        assert spec.path == 'datapkgdemo', spec.path

    def test_02_parse_spec_ckan_3(self):
        spec = Spec.parse_spec('ckan://test.ckan.net/api/datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.netloc == 'http://test.ckan.net/api', spec.netloc
        assert spec.path == 'datapkgdemo', spec.path

    def test_02_parse_spec_ckan_1(self):
        spec = Spec.parse_spec('db://datapkgdemo')
        assert spec.scheme == 'db', spec.scheme
        assert spec.path == 'datapkgdemo', spec.path

    def test_03_parse_spec_default(self):
        spec = Spec.parse_spec('datapkgdemo')
        assert spec.scheme == 'file', spec.scheme
        assert spec.path == 'datapkgdemo', spec.path

    def test_04_index_from_spec(self):
        from datapkg.index.base import FileIndex
        spec = Spec.parse_spec(self.file_spec)
        index, path = spec.index_from_spec()
        assert isinstance(index, FileIndex)

        spec = Spec.parse_spec('file://.')
        index, path = spec.index_from_spec()
        assert isinstance(index, FileIndex)

    def test_04_index_from_spec_ckan(self):
        from datapkg.index.ckan import CkanIndex
        spec = Spec.parse_spec('ckan://datapkgdemo')
        index, path = spec.index_from_spec()
        assert isinstance(index, CkanIndex)

    def test_04_index_from_spec_db(self):
        from datapkg.index.db import DbIndexSqlite
        spec = Spec.parse_spec('db://datapkgdemo')
        index, path = spec.index_from_spec()
        assert isinstance(index, DbIndexSqlite)

