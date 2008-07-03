import setuptools
import setuptools.dist
import zipimport, os
from pkg_resources import PathMetadata, EggMetadata
from pkg_resources import Distribution

class PyPkgTools(object):

    def load_distribution(self, pkg_path):
        # Follows setuptools.command.easy_install.easy_install.egg_distribution.
        if os.path.isdir(pkg_path):
            egginfo_path = os.path.join(pkg_path, 'EGG-INFO')
            possibilities = [ egginfo_path ]
            possibilities += [ os.path.join(pkg_path, x) for x in filter(lambda x: x.endswith('.egg-info'), os.listdir(pkg_path)) ]
            metadata = None
            for path in possibilities:
                if os.path.exists(path):
                    metadata = PathMetadata(pkg_path, path)
                    break
            if metadata is None:
                raise
                  
        else:
            metadata = EggMetadata(zipimport.zipimporter(pkg_path))
        return Distribution.from_filename(pkg_path, metadata=metadata)
	
    def read_pkg_name(self, path):
        dist = self.load_distribution(path)
        print dist.__dict__
        return dist.key



