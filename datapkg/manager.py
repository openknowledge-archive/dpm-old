'''The Package Manager which handles all general package features (index,
search) plus installation and removal of packages in the local repository.

Note that actual installation and removal is delegated to Package object to
allow for multiple types of package (and natural OO reasons!).

Idea: handle the index in a mercurial repository so we can pull from elsewhere
etc. This avoids us having to handle all the syncing stuff.
'''
import os
import ConfigParser

import datapkg
from datapkg.package import PackagePlain

class PackageManager(object):

    def __init__(self, system_path=None):
        if system_path is None:
            system_path = os.path.join(os.path.expanduser('~'), '.datapkg')
        self.system_path = os.path.abspath(os.path.expanduser(system_path))
        self.config_path = os.path.join(self.system_path, 'config.ini')
        self.index_path = os.path.join(self.system_path, 'index')
        self.installed_path = os.path.join(self.system_path, 'installed')
        self.index = None
        self.load_index()

    def init(self):
        if not os.path.exists(self.system_path):
            os.makedirs(self.system_path)
            cfg = ConfigParser.SafeConfigParser()
            cfg.set('DEFAULT', 'version', datapkg.__version__)
            cfg.write(file(self.config_path, 'w'))
            # TODO: use mercurial from python
            cmd = 'hg init %s' % self.index_path
            os.system(cmd)
        else:
            msg = 'init() failed. It looks like you have already ' + \
                    'initialised a datapkg repository at %s' % self.system_path
            raise ValueError(msg)

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
                    results.append(PackagePlain(pkg['id'], **pkg))
        return results

    def install(self, name):
        pkgasdict = self.index[name]
        pkg = PackagePlain(pkgasdict['id'], **pkgasdict)
        pkg.install(self.installed_path)
        # TODO: ? mark package as installed in the index

    def install_not_from_index(self, url, type=None):
        '''Install a package that is not yet in the index (e.g. direct from
        url).'''
        # take package name from file name
        # TODO: proper filename generation
        # file-name must not have
        # TODO: finish
        name = os.url.split('/')[-1]
        # if not type:
        # TODO: set type correctly
        pkg = PackagePlain(name, type=type)


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


def pkg_name_from_file_name(filename):
    pass

