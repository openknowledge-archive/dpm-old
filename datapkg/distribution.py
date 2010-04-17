'''A `Distribution` is a serialization of a `Package` to disk.
''' 
import os

from datapkg import DatapkgException
from datapkg.package import Package
import datapkg.metadata as M

default_distribution_name = 'datapkg.distribution:IniBasedDistribution'

def default_distribution():
    import datapkg.distribution
    modpath, klassname = datapkg.distribution.default_distribution_name.split(':')
    mod = __import__(modpath, fromlist=['anyoldthing'])
    klass = getattr(mod, klassname)
    return klass

def load(path):
    '''Load distribution at path.
    
    Cycle through all available distribution types trying to load using each on
    in turn return first one which works.
    '''
    # TODO: replace this with something more pluggable e.g. from entry_points
    distributions = [ PythonDistribution, IniBasedDistribution ]
    errors = []
    for klass in distributions:
        try:
            dist = klass.load(path)
            return dist
        except Exception, inst:
            errors.append(str(inst))
    msg = 'Failed to load distribution from %s\n%s' % (path, errors)
    raise DatapkgException(msg)


class DistributionBase(object):
    # distribution_type = None

    def __init__(self, package=None):
        self.package = package

    def write(self, path, **kwargs):
        '''Write this distribution to disk at `path`.
        '''
        raise NotImplementedError

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.
        
        @return: the package object.
        '''
        raise NotImplementedError

    def stream(self, path):
        '''Return a fileobj stream for material at `path`.
        '''
        raise NotImplementedError


class PythonDistribution(DistributionBase):

    # TODO: write should write out package metadata ...
    def write(self, path, template='default'):
        '''See parent.

        @param template: paster template to use
        '''
        # TODO: import PasteScript direct and use
        # use no-interactive to avoid querying on vars
        cmd = 'paster create --no-interactive --template=datapkg-%s ' % template
        base_path, xxx = Package.info_from_path(path)
        if base_path:
            cmd += '--output-dir %s ' % base_path
        cmd += self.package.name
        # TODO: catch stdout and only print if error
        import commands
        # os.system(cmd)
        import datapkg.util
        status, output = datapkg.util.getstatusoutput(cmd)
        if status:
            msg = 'Error on attempt to create file structure:\n\n%s' % output
            raise DatapkgException(msg)
        return self.package.installed_path

    @classmethod
    def load(self, path):
        '''Load a L{Package} object from a path to a package distribution.'''
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(path)
        metadata = M.MetadataConverter.from_distutils(pydist.metadata)
        pkg = Package(name=pydist.metadata.name, installed_path=unicode(path))
        pkg.update_metadata(metadata)
        pkg.manifest = dict([ (x,None) for x in pydist.filelist])
        dist = self(pkg)
        return dist

    def is_python_distribution(self, path):
        # taken from easy_install.install_item
        # could just have tried to install and caught exception
        dist_filename = path
        setup_base = path
        if dist_filename.lower().endswith('.egg'):
            return True
        elif dist_filename.lower().endswith('.exe'):
            return True
        setup_script = os.path.join(setup_base, 'setup.py')
        if os.path.exists(setup_script):
            return True
        return False

    def make_python_distribution(self, base_path, package_files):
        dist_path = self.create_file_structure(base_path)
        pypkg_inside_pkg_dir = os.path.join(dist_path, self.name)
        if os.path.isdir(package_files):
            for fn in os.listdir(package_files):
                path = os.path.join(package_files, fn)
                # TODO: move rather than copy?
                if os.path.isdir(path):
                    shutil.copytree(path, pypkg_inside_pkg_dir)
                else:
                    shutil.copy(path, pypkg_inside_pkg_dir)
        else:
            shutil.copy(package_files, pypkg_inside_pkg_dir)
        return dist_path

    def install(self, install_dir, local_path_to_package_files=None, **kwargs):
        dist_path = local_path_to_package_files
        import distutils.errors
        import tempfile
        # TODO: cleanup ...
        tmpdir = tempfile.mkdtemp('datapkg-')
        if not local_path_to_package_files:
            if self.download_url:
                dist_path = self.download(tmpdir)
            else:
                msg = 'No package files to install and no download url either'
                raise Exception(msg)

        # support case where what we have is not yet a python package
        extract_dir = os.path.join(tmpdir, 'extract')
        if not self.is_python_distribution(dist_path):
            dist_path = self.unpack(dist_path, extract_dir)
            if not self.is_python_distribution(dist_path):
                # this will create tmpdir/{self.name}
                # so need to be sure that download file not named self.name
                # to ensure no conflict when we do this
                dist_path = self.make_python_distribution(tmpdir, extract_dir)
        else:
            dist_path = local_path_to_package_files
        self.install_python_package(install_dir, dist_path, tmpdir, **kwargs)

    def install_python_package(self, install_dir, pkg_path, tmpdir,
            zip_safe=False):
        import datapkg.pypkgtools
        pydist = datapkg.pypkgtools.load_distribution(pkg_path)
        installed_path = pydist.install(install_dir, tmpdir, zip_safe)
        self.package.installed_path = installed_path
    
    def stream(self, path):
        # TODO: should move to using underlying pydist here ...
        import sys
        sys.path.insert(0, self.package.installed_path)
        import pkg_resources
        return pkg_resources.resource_stream(self.package.name, path)


import ConfigParser
class IniBasedDistribution(DistributionBase):
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
 
    def stream(self, path):
        full_path = os.path.join(self.package.installed_path, path)
        return open(full_path)

