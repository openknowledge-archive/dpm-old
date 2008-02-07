import os
import ConfigParser

from package import Package

class PackageManager(object):

    def __init__(self, cache_path='~/var/lib/datapkg/default'):
        self.cache_path = os.path.abspath(os.path.expanduser(cache_path))
        self.index_path = os.path.join(self.cache_path, 'index.ini')
        self.installed_path = os.path.join(self.cache_path, 'installed')
        self.index = None
        self.load_index()

    def load_index(self):
        self.index = self._get_index_as_dict()

    def update_index(self, index_fileobj):
        # let's just hack it for the time being
        indexfo = file(self.index_path, 'w')
        indexfo.write('\n\n')
        indexfo.write(index_fileobj.read())
        indexfo.close()
        # need to reload due to changes
        self.load_index()

    def search(self, search_str):
        allpkgs = self._get_index_as_dict(file(self.index_path))
        results = []
        for pkg in allpkgs.values():
            for k,v in pkg.items():
                if search_str in v:
                    results.append(Package(pkg['id'], **pkg))
        return results

    def install(self, name):
        pkgasdict = self.index[name]
        pkg = Package(pkgasdict['id'], **pkgasdict)
        pkg.install(self.installed_path)
        # TODO: ? mark package as installed in the index

    def __len__(self):
        return len(self.index)

    def _get_index_as_dict(self, index_fileobj=None):
        if not index_fileobj:
            if os.path.exists(self.index_path):
                index_fileobj = file(self.index_path)
            else:
                return []
        cfgparser = ConfigParser.SafeConfigParser()
        cfgparser.readfp(index_fileobj)
        results = {}
        for section in cfgparser.sections():
            outdict = dict(cfgparser.items(section))
            outdict['id'] = section
            results[section] = outdict
        return results


