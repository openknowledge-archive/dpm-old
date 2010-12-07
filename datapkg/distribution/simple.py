import os
import ConfigParser

from datapkg.package import Package
import datapkg.metadata as M
from base import DistributionBase


class SimpleDistribution(DistributionBase):
    '''Simple distribution storing metadata in an ini file.

    File layout::

        {dist-path}/metadata.txt
    
          * metadata.txt: package metadata in ini-file format (key = value or
            key: value with support for line continuations). See
            http://docs.python.org/library/configparser.html.
          * Manifest items are inserted as sections with name of ile and prefix
            'manifest::' e.g. [manifest::myfilename.csv]

        {dist-path}/....

            # Data (and code): any files you want (specify them in the
            # manifest).
    '''
    manifest_prefix = 'manifest::'
    keymap = {
        'id': 'name',
        'creator': 'author',
        'description': 'notes',
        'comments': 'notes',
        'licence': 'license',
        'tags': 'keywords',
        }

    @classmethod
    def load(self, path):
        pkg = Package()
        pkg.installed_path = path 
        fp = os.path.join(path, 'metadata.txt')
        # Read metadata from config.ini style fileobj
        cfp = ConfigParser.SafeConfigParser()
        cfp.readfp(open(fp))
        # TODO: utf8 to unicode conversion?
        filemeta = cfp.defaults()
        newmeta = M.MetadataConverter.normalize_metadata(filemeta,
                keymap=self.keymap)
        pkg.update_metadata(newmeta)
        for section in cfp.sections():
            if section.startswith(self.manifest_prefix):
                filepath = section[len(self.manifest_prefix):]
                pkg.manifest[filepath] = dict(cfp.items(section))
        # TODO: manifest approach (i.e. walk the directory looking for material)
        for fn in ['data.csv', 'data.js']:
            fullpath = os.path.join(pkg.installed_path, fn)
            if os.path.exists(fullpath) and not fn in pkg.manifest:
                pkg.manifest[fn] = None
        return self(pkg)

    def write(self, path, **kwargs):
        '''Writes distribution to disk.
        
        Metadata written to metadata.txt in ini style (python ConfigParser)
        with encoding to utf8.
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        meta_path = os.path.join(path, 'metadata.txt')
        # use RawConfigParser to avoid magical interpolation feature (and hence
        # issues with %s in data)
        cfp = ConfigParser.RawConfigParser()
        for k,v in self.package.metadata.items():
            cfp.set('DEFAULT', k, unicode(v).encode('utf8'))
        for filepath, metadata in self.package.manifest.items():
            section = self.manifest_prefix + filepath
            cfp.add_section(section)
            if metadata:
                for k,v in metadata.items():
                    # TODO: (?) json dump of v
                    # will be weird for text values json.dumps('x') => '"x"'
                    cfp.set(section, k, unicode(v).encode('utf8'))
        fo = file(meta_path, 'w')
        cfp.write(fo)
        fo.close()
 

# 2010-10-11 - added for backwards compatibility
IniBasedDistribution = SimpleDistribution

