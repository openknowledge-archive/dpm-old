from ConfigParser import ConfigParser
try: from cStringIO import StringIO
except ImportError: from StringIO import StringIO
import pkg_resources

from datapkg.index.base import IndexBase
from datapkg.package import Package
from datapkg.metadata import Metadata

class EggIndex(IndexBase):
    """
    This class treats an installed python package as a data
    index. For instructions on creating such a package, what
    needs to go in its setup.py and such, see 
    :func:`datapkg.pypkgtools.datapkg_index`. Here we are
    concerned with how to use such a package.

    An example of one such package can be installed like so::

        % pip install hg+http://bitbucket.org/ww/ukgov_treasury_cra

    Once installed, datapkg can be used to inspect it and 
    install parts wherever desired::

        % datapkg list egg://ukgov_treasury_cra
        cra2009 -- Country and Regional Analysis 2009
        % datapkg install egg://ukgov_treasury_cra/cra2009 file:///tmp
        [...]
        % ls -l /tmp/cra2009/ 
        total 11112
        -rw-r--r--  1 ww  wheel  5681852 May 12 15:48 cra_2009_db.csv
        -rw-r--r--  1 ww  wheel      292 Aug 17 22:37 metadata.txt
    """
    def __init__(self, name):
        try:
            dist = pkg_resources.get_distribution(name)
            sources = dist.get_metadata("datapkg_index.txt")
        except pkg_resources.DistributionNotFound:
            raise KeyError("No installed python package named %s" % name)
        except IOError:
            raise KeyError("No data sources in %s" % name)
        self.index = ConfigParser()
        self.index.readfp(StringIO(sources))

    def list(self):
        return [self.get(name) for name in self.index.sections()]

    def get(self, name):
        kwargs = dict((k, self.index.get(name, k)) 
                      for k in self.index.options(name)
                      if k in Metadata.key_list)
        kwargs["name"] = name
        pkg = Package(**kwargs)
        pkg.extras.update((k, self.index.get(name, k))
                          for k in self.index.options(name)
                          if k not in Metadata.key_list)
        return pkg

    def search(self, query):
        query = query.lower()
        for package in self.list():
            if query in package.name.lower() or query in package.title.lower():
                yield package

    def has(self, name):
        return name in self.index.sections()
