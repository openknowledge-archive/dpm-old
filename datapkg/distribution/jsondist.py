import os
try:
    import json
except ImportError:
    import simplejson as json

from datapkg.package import Package
from base import DistributionBase

class JsonDistribution(DistributionBase):
    '''Simple distribution storing metadata in json files.

        {dist-path}/package.json
    
          * package metadata in json format.

        {dist-path}/manifest.json

          * Manifest items

        {dist-path}/....

            # Data (and code): any files you want (specify them in the
            # manifest).

    '''
    metadata_filename = 'package.json'
    manifest_filename = 'manifest.json'

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.
        
        @return: the Distribution object.
        '''
        pkg = Package()
        pkg.installed_path = path 
        metadata_path = os.path.join(path, self.metadata_filename)
        manifest_path = os.path.join(path, self.manifest_filename)
        fo = open(metadata_path)
        pkg.update_metadata(json.load(fo))
        fo.close()
        if os.path.exists(manifest_path):
            fo = open(manifest_path)
            pkg.manifest = json.load(fo)
            fo.close()
        return self(pkg)

    def write(self, path, **kwargs):
        '''Write this distribution to disk at `path`.
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        metadata_path = os.path.join(path, self.metadata_filename)
        manifest_path = os.path.join(path, self.manifest_filename)
        fo = open(metadata_path, 'w')
        json.dump(self.package.metadata, fo, indent=2, sort_keys=True)
        fo.close()
        fo = open(manifest_path, 'w')
        json.dump(self.package.manifest, fo, indent=2, sort_keys=True)
        fo.close()

