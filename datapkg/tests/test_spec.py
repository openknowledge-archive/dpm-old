from datapkg.spec import *

from datapkg.tests.base import TestCase


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

    def test_01_parse_spec_1(self):
        cwd = os.getcwd()
        spec = Spec.parse_spec('file://')
        assert spec.scheme == 'file'
        assert spec.netloc == os.path.dirname(cwd), spec
        assert spec.path == os.path.basename(cwd), spec

    def test_01_parse_spec_2(self):
        path = os.getcwd()
        spec = Spec.parse_spec('.')
        assert spec.scheme == 'file'
        assert spec.netloc == os.path.dirname(path), spec
        assert spec.path == os.path.basename(path), spec.path

    def test_01_parse_spec_3(self):
        spec = Spec.parse_spec(self.index_spec)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.path == os.path.basename(self.repo_path)

    def test_01_parse_spec_4(self):
        spec = Spec.parse_spec(self.repo_path)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.path == os.path.basename(self.repo_path)

    def test_01_parse_spec_5(self):
        spec = Spec.parse_spec(self.repo_path, all_index=True)
        assert spec.scheme == 'file', (spec.scheme,spec.netloc,spec.path)
        assert spec.netloc == self.repo_path
        assert spec.path == ''

    def test_01_parse_spec_ckan_1(self):
        spec = Spec.parse_spec('ckan:datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.path == 'datapkgdemo', spec.path

    def test_01_parse_spec_ckan_2(self):
        spec = Spec.parse_spec('ckan://datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.netloc == '', spec.netloc 
        assert spec.path == 'datapkgdemo', spec.path

    def test_01_parse_spec_ckan_3(self):
        spec = Spec.parse_spec('ckan://test.ckan.net/api/datapkgdemo')
        assert spec.scheme == 'ckan', spec.scheme
        assert spec.netloc == 'http://test.ckan.net/api', spec.netloc
        assert spec.path == 'datapkgdemo', spec.path

    def test_3_index_from_spec(self):
        import datapkg.index
        spec = Spec.parse_spec(self.file_spec)
        index, path = spec.index_from_spec()
        assert isinstance(index, datapkg.index.FileIndex)

        spec = Spec.parse_spec('.')
        index, path = spec.index_from_spec()
        assert isinstance(index, datapkg.index.FileIndex)

