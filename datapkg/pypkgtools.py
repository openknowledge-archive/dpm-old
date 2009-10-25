'''Interface to Distutils/Setuptools code.

Provide a simple Distribution object (`DistributionOnDiskBase`) providing
access to a python distribution's metadata (PKG-INFO and MANIFEST/SOURCES.txt).

General Remarks on Setuptools Etc
=================================

PkgResources and Setuptools can be difficult for the uninitiated to grapple
with (putting it politely).

For us the most fundamental problem is that there is, at present, no simple way
to get metadata about a distribution on disk (whether installed or just in raw
source form) and one has to hack around with various different approaches. What
one would **really, really** like is an interface like::

    pydist = Distribution(path_on_disk)

As of 2009-08-12 there is hope that this is going to be addressed -- see PEP
376 http://www.python.org/dev/peps/pep-0376/.

2009-10-25: see also this recent thread:

http://mail.python.org/pipermail/distutils-sig/2009-July/012765.html

This also could be useful: http://pypi.python.org/pypi/pkginfo/

More Details
------------

Things are also confused by different objects having the same
or similar names. For example a pkg_resources Distribution object is very
different from a setuptools.core.Distribution object (which is like the
distutils one).

Also rather confusingly PkgResources ends up making its metadata objects into
providers (i.e. a provider *has* metadata but simultaneously metadata isa
provider ...).

Similarly, behind the scenes in pkg_resources a Distribution delegates all main
functionality to its associated provider/metadata object. Furthermore, a
metadata object is not actually metadata itself but a pointer to a collection
of metadata directories and files.
'''
import zipimport, os
import StringIO
import logging

logger = logging.getLogger(__file__)

import setuptools
import setuptools.dist
import setuptools.package_index as pi
import setuptools.command.easy_install

def load_distribution(dist_path):
    '''Given a path return an appropriate DistributionOnDisk* instance
    '''
    built_egg_info = os.path.join(dist_path, 'EGG-INFO')
    setuppy = os.path.join(dist_path, 'setup.py')
    if not os.path.isdir(dist_path): # A.1
        return DistributionOnDiskEgg(dist_path)
    elif os.path.exists(built_egg_info): # A.2
        return DistributionOnDiskEggUnpacked(dist_path)
    else:
        egginfos = filter(lambda x: x.endswith('.egg-info'),
            os.listdir(dist_path))
        if len(egginfos) > 0: # B.1
            return DistributionOnDiskEggSource(dist_path)
        elif os.path.exists(setuppy): # B.2
            return DistributionOnDiskRawSource(dist_path)
    msg = 'File/Directory at %s does not look like a Distribution' % dist_path
    raise ValueError(msg)


class DistributionOnDiskBase(object):
    '''Wrap a python distribution on disk.

    @attrib metadata: distribution metadata (i.e. contents of PKG-INFO).
        Returned in the form of a distutils.dist.Distribution. Main metadata
        attributes are then accessible directly via property calls.
    @attrib filelist: list of files (corresponds to SOURCES.txt). Returns as a
    python list of file names.

    # 4 possible cases:
    # A.1: built distribution zipped
    # A.2: built distbn unzipped
    # B.1: a development/unbuilt distribution with a .egg-info directory
    # B.2: a raw distribution (no egg, nothing more than a setup.py ...)

    These are handled by separate child classes.
    '''
    def __init__(self, dist_path):
        self.dist_path = dist_path
        self.metadata = None
        self.filelist = []
        self._init()
        self.name = self.metadata.name

    def read_pkg_name(self, path):
        return self.metadata.name

    def parse_pkg_info(self, fileobj):
        '''Parse PKG-INFO fileobj and return DistributionMetadata object.
        
        task is to invert distutils.dist.DistributionMetadata.write_pkg_file

        Partially based on http://mail.python.org/pipermail/distutils-sig/2007-June/007783.html
        '''
        from distutils.dist import DistributionMetadata
        metadata = DistributionMetadata()
        # description in setup.py is summary in egg-info!
        fields = list(metadata._METHOD_BASENAMES) + ['summary']

        import rfc822
        message =rfc822.Message(fileobj)
        for name, value in message.items():
            field = name.lower().replace('-', '_')
            setattr(metadata, field, value)
        return metadata

    def get_filelist(self):
        import setuptools.command.egg_info
        # can do this 2 ways 

    # could make this a class method
    def install(self, install_dir, tmpdir, zip_safe=False):
        '''Install a python distribution at {pkg_path} to {install_dir} using
        easy_install and return the path to which it was installed.

        Can be run from Base class (i.e. does not require that this is a 'real'
        distribution).

        In essence emulates::

            easy_install --multi-version --install-dir install_dir dist_path
        '''
        pkg_path = self.dist_path

        # setuptools stuff
        self.pi = pi.PackageIndex('http://random.url/')
        tdist = setuptools.dist.Distribution()
        self.easy_install = setuptools.command.easy_install.easy_install(tdist)

        self.easy_install.install_dir = install_dir
        self.easy_install.multi_version = True
        self.easy_install.zip_ok = zip_safe
        # Suppress easy_install.installation_report() messages
        # (o/w receive confusing report at end of install about multi-version
        # etc)
        self.easy_install.no_report = True
        # hack to make finalize_options happy
        self.easy_install.args = True
        self.easy_install.finalize_options()
        install_needed = True
        deps = False
        # taken from easy_install.install_item
        spec = None
        dists = self.easy_install.install_eggs(spec, pkg_path, tmpdir)
        for dist in dists:
            # better have only one dist!
            installed_path = dist.location
            self.easy_install.process_distribution(spec, dist, deps)
            return installed_path

    def _build_egg_info(self, dist_path):
        # WARNING none of this works if we don't have permission to write to
        # source directory ...
        current_dir = os.getcwd()
        try:
            os.chdir(self.dist_path)
            # fails with
            # DistutilsFileError: package directory 'datapkg' does not exist
            # distutils_dist.run_command('egg_info')
            # also fails ...
            # import setuptools.command.egg_info as egg_info
            # cmd = egg_info.egg_info(distutils_dist)
            # cmd.run()

            # this is done right in pip.py run_egg_info function ...
            cmd = 'python setup.py -q egg_info'
            notok = os.system(cmd)
            assert not notok, 'RawSource: Failed to build egg_info so manifest may be unavailable'
            tmpdist = DistributionOnDiskEggSource(self.dist_path)
            self.filelist = tmpdist.filelist
        except Exception, inst:
            logger.error(inst)
        finally:
            os.chdir(current_dir)


class DistributionOnDiskRawSource(DistributionOnDiskBase):
    '''A raw source distribution on disk (i.e. with a setup.py file.
    '''

    def _init(self):
        distutils_dist = self._get_distutils_dist(self.dist_path)
        self.metadata = distutils_dist.metadata
        # normalize metadata (seems to be slightly different ...)
        if self.metadata.keywords:
            self.metadata.keywords = ' '.join(self.metadata.keywords)
        self.filelist = []

        self._build_egg_info(self.dist_path)
        try: # this may fail if build_egg_info fails
            tmpdist = DistributionOnDiskEggSource(self.dist_path)
            self.filelist = tmpdist.filelist
        except ValueError, inst:
            logger.error(inst)

    def _get_distutils_dist(self, dist_path):
        '''Get a distutils.dist.Distribution instance associated to setup.py in
        dist_path.'''

        '''Get metadata from a setup.py file.'''
        setuppy = os.path.join(self.dist_path, 'setup.py')
        import distutils.core
        dist = distutils.core.run_setup(setuppy, stop_after='init')
        return dist

    def listdir(self, path):
        fullpath = os.path.join(self.dist_path, path)
        return os.listdir(fullpath)

    def resource_stream(self, path):
        fullpath = os.path.join(self.dist_path, path)
        return open(fullpath)


import pkg_resources
class DistributionOnDiskEgg(DistributionOnDiskBase):
    '''Wrap an EGG distribution on disk.

    In essence this is a wrapper around pkg_resources.Distribution object.
    '''

    def _init(self):
        self.pkgr_metadata = self._load_pkgr_metadata()
        self.pkgr_dist = pkg_resources.Distribution.from_filename(self.dist_path,
                metadata=self.pkgr_metadata)
        pkg_info = StringIO.StringIO(self.pkgr_metadata.get_metadata('PKG-INFO'))
        self.metadata = self.parse_pkg_info(pkg_info)
        sources = self.pkgr_metadata.get_metadata('SOURCES.txt')
        self.filelist = sources.split('\n')

    def _load_pkgr_metadata(self):
        metadata_finder = pkg_resources.EggMetadata(zipimport.zipimporter(self.dist_path))
        return  metadata_finder

    def listdir(self, path):
        return self.pkgr_dist.resource_listdir(path)
    
    def resource_stream(self, path):
        # do not appear to need a manager ...
        # might do if we were doing extraction I guess ...
        # another reason to always work unzipped ...
        manager = None
        return self.pkgr_dist.get_resource_stream(manager, path)


class DistributionOnDiskEggUnpacked(DistributionOnDiskEgg):
    
    def _load_pkgr_metadata(self):
        built_egg_info = os.path.join(self.dist_path, 'EGG-INFO')
        metadata_finder = pkg_resources.PathMetadata(self.dist_path, built_egg_info)
        return  metadata_finder


class DistributionOnDiskEggSource(DistributionOnDiskEgg):
    def _load_pkgr_metadata(self):
        # Doesn't work! Leads to infinite recursion ...
        # rebuild egg_info so that we pick up any changed metadata
        # self._build_egg_info(self.dist_path)

        egginfos = filter(lambda x: x.endswith('.egg-info'),
                os.listdir(self.dist_path))
        if not len(egginfos) > 0:
            msg = 'Cannot load Distribution as no *.egg-info file found at %s' % self.dist_path
            raise ValueError(msg)
        # take first one
        egg_info = os.path.join(self.dist_path, egginfos[0])
        metadata_finder = pkg_resources.PathMetadata(self.dist_path, egg_info)
        return  metadata_finder

