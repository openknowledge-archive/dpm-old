'''Download packages (or, more accurately, their resources).
'''
import logging
import fnmatch

import pkg_resources

import dpm.util

logger = logging.getLogger('dpm.download')


class PackageDownloader(object):
    '''Download packages (and their related resources).
    
    Basic process:
        1. Get package from source index/destination
        2. Read through resources and see if there is a 'dpm'
            distribution
            * If yes use that
            * If no prompt for downloading of each resource item
    '''

    def __init__(self, verbose=False):
        self.verbose = verbose

    def _print(self, msg):
        logger.debug(msg)
        if self.verbose:
            print msg

    def download(self, pkg, dest_path, filterfunc=None):
        '''Download the package to disk (i.e. metadata plus resources)

        :param pkg: the package object
        :param dest_path: the path to download to
        :param filterfunc: [optional] a function filterfunc(resource,
        order) applied to each package resource together with its order
        (0,1,...) in the list of package resources that determines whether a
        download is attempted by returning True (download) or False (no
        download).
                           If not provided download all resources.
        '''
        # download everything
        if filterfunc is None:
            filterfunc = lambda x,y: True

        self._print('Creating package metadata')
        # cribbed from dpm/index/base.py:FileIndex
        import dpm.distribution
        dist = dpm.distribution.default_distribution()(pkg)
        dist.write(dest_path)

        self._print('Downloading package resources to %s ...' % dest_path)

        if not pkg.resources:
            msg = u'Warning: no resources to install for package'
            self._print(msg)

        # reset this attribute for interactive filterfunc
        self._interactive_status = None
        for count, resource in enumerate(pkg.resources):
            if filterfunc(resource, count):
                self.download_resource(resource, count, dest_path)
            else:
                self._print('Skipping package resource: %s' % resource['url'])
        
    def download_resource(self, resource, count, dest_path):
        self._print('Downloading package resource: %s' % resource['url']) 

        success = False
        for entry_point in pkg_resources.iter_entry_points('dpm.resource_downloader'):
            downloader_cls = entry_point.load()
            downloader = downloader_cls()
            success = downloader.download(resource, dest_path)
            if success:
                break
        if not success:
            self._print('Unable to retrieve resource: %s' % resource)
            return None
        else:
            return success

    def filterfunc_interactive_choice(self, resource, count):
        '''A filterfunc that interacts with user to determine whether to
        download the resource.
        '''
        if self._interactive_status != None:
            return self._interactive_status
        msg = ' Do you want to retrieve this resource? (y/n/a/q/?: '
        retrieve = None
        while(retrieve not in ['y', 'n', 'a', 'q']):
            self._print(' Resource: [%s] %s\n  %s' % (
                resource.get('format', ''),
                resource['url'],
                resource.get('description', '') or 'No description ...'
                ))
            retrieve = raw_input(msg)
            retrieve = retrieve.lower()
            if retrieve == '?':
                help_ = 'y = yes, no = no, '
                help_ += 'a = yes to this and all following, '
                help_ += 'q = quit (no to this and all following)'
                print help_
            elif retrieve == 'y':
                return True
            elif retrieve == 'n':
                return False
            elif retrieve == 'a':
                self._interactive_status = True
                return True
            elif retrieve == 'q':
                self._interactive_status = False
                return False

    @classmethod
    def make_glob_filterfunc(self, formatpat, urlpat='*'):
        '''Make a filter function based on a glob-style format_pattern and
        url_pattern'''
        def filterfunc(resource, count):
            match = fnmatch.fnmatch(resource.get('format', '').lower(),
                    formatpat)
            match = match and fnmatch.fnmatch(resource['url'], urlpat)
            return match
        return filterfunc


class ResourceDownloaderBase(object):
    '''Base class for (package) resource downloaders which handle the
    downloading or accessing of (package) resources (i.e. files containing
    package data, APIs to package data etc).

    To create a new resource downloader and have it used by dpm:

      1. Create a new class inheriting from
      :class:`dpm.download.ResourceDownloaderBase`

      2. Add an entry point in the [dpm.resource_downloader] entry_points section of
      your setup.py pointing to this class.

    Many downloaders can be installed to handle different types of resources.
    Installed downloaders are called in turn with the first one to match being
    used. The order of calling is determined by order ot
    pkg_resources.iter_entry_points for the dpm.resource_downloader entry
    point.
    '''

    def download(self, resource, dest_path):
        '''Download the supplied resource.

        Should be overriden (and not called) by inheriting classes.

        This method should return True if and only if the class can handle
        (and therefore has handled) the downloaded resource and should return False otherwise
        (thereby allowing subsequent downloaders to be tried).
        '''
        raise NotImplementedError
    

class ResourceDownloaderSimple(ResourceDownloaderBase):
    '''Simple resource downloader that retrieves remote files using urllib.'''

    def download(self, resource, dest_path):
        url = resource['url']
        format_ = resource.get('format', '')
        format_type = format_.split('/')[0]
        if format_type in [ 'api', 'services' ]:
            return False
        else: # treat everything as a retrievable file ...
            downloader = dpm.util.Downloader()
            downloader.download(url, dest_path)
            return True

