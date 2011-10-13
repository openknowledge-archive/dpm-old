import dpm.metadata as M
import distutils.dist

class TestMetadataConverter:
    def test_1(self):
        inmeta = distutils.dist.DistributionMetadata()
        inmeta.name = 'XXX'
        inmeta.description = 'xyz'
        inmeta.long_description = '''A whole bunch of stuff ...'''
        outmeta = M.MetadataConverter.from_distutils(inmeta)
        assert outmeta['title'] == 'xyz', outmeta
        assert outmeta['name'] == 'XXX'
        assert outmeta['notes'] == inmeta.long_description, outmeta

    def test_with_summary(self):
        inmeta = distutils.dist.DistributionMetadata()
        inmeta.name = 'XXX'
        inmeta.summary = 'YYY'
        inmeta.description = 'xyz'
        outmeta = M.MetadataConverter.from_distutils(inmeta)
        assert outmeta['name'] == 'XXX'
        assert outmeta['title'] == 'YYY'
        assert outmeta['notes'].endswith(inmeta.description), outmeta
    
    def test_normalize_metadata_strip_empty_extras(self):
        # these are keys that distutils provides by default
        inmeta = { 'provides':  u'' }
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        assert 'provides' not in outmeta['extras'], outmeta

    def test_normalize_metadata_tags(self):
        exp = [u'tag1', u'tag2']

        inmeta = { 'tags':  exp }
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        assert outmeta['tags'] == exp, outmeta

        inmeta = { 'tags':  u'tag1, tag2' }
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        assert outmeta['tags'] == exp, outmeta

        inmeta = { 'tags':  u"[u'tag1', u'tag2']" }
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        assert outmeta['tags'] == exp, outmeta

    def test__standardize_distutils(self):
        inmeta = distutils.dist.DistributionMetadata()
        inmeta.home_page = 'http://xyz.com'
        outmeta = M.MetadataConverter.from_distutils(inmeta)
        assert outmeta['url'] == inmeta.home_page, outmeta

    def test_tags_are_normalized(self):
        inmeta = { 'tags':  u'be here,now, everyone' }
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        assert outmeta['tags'] == ['be', 'here', 'now', 'everyone'], outmeta['tags']

    def test_download_resource(self):
        inmeta = {'download_url': 'http://xyz.com'}
        outmeta = M.MetadataConverter.normalize_metadata(inmeta)
        outmeta['resources'][0]['url'] = inmeta['download_url']

