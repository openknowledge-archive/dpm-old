import datapkg.metadata as M
import distutils.dist

class TestMetadataConverter:
    def test_1(self):
        inmeta = distutils.dist.DistributionMetadata()
        inmeta.name = 'XXX'
        inmeta.description = 'xyz'
        outmeta = M.MetadataConverter.from_distutils(inmeta)
        assert outmeta['title'] == 'xyz'
        assert outmeta['name'] == 'XXX'
        assert outmeta['notes'] == '', outmeta

