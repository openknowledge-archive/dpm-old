from dpm.tests.base import *
from dpm.distribution import DistributionBase, JsonDistribution
from dpm.package import Package


import json
class TestJsonDistribution(TestCase):
    def setUp(self):
        self.tmpdir = self.make_tmpdir()
        self.installdir = os.path.join(self.tmpdir, 'installed')
        self.loaddir = os.path.join(self.tmpdir, 'load')
        os.makedirs(self.loaddir)
        self.pkg_name = 'mytestpkg'
        self.pkg = Package(name=self.pkg_name, version='1.0')
        self.dist = JsonDistribution(self.pkg)

    def test_write(self):
        self.dist.write(self.installdir)
        meta = os.path.join(self.installdir, 'datapackage.json')
        assert os.path.exists(meta), os.listdir(self.installdir)
        metadata = json.load(open(meta))
        assert metadata['name'] == self.pkg_name

    def test_load(self):
        metafp = os.path.join(self.loaddir, 'datapackage.json')
        datadict = {
            'name': u'abc',
            'title': 'These are the Jones',
            'resources': [
                {'url': 'http://xyz.com', 'format': 'csv'}
                ]
            }
        print 'XXX', metafp
        json.dump(datadict, open(metafp, 'w'))
        dist = JsonDistribution.load(self.loaddir)
        assert dist.package.name == u'abc'
        assert dist.package.resources[0]['format'] == 'csv'

