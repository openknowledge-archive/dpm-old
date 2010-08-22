'''Download packages (or, more accurately, their resources).
'''
import logging

import pkg_resources

import datapkg.util

logger = logging.getLogger('datapkg.download')


class PackageDownloader(object):
    '''
    Basic process:
        1. Get package from source index/destination
        2. Read through resources and see if there is a 'datapkg'
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

    def download(self, pkg, dest_path):
        self._print('Downloading package to: %s' % dest_path)
        if not pkg.resources:
            msg = u'Warning: no resources to install for package' % pkg.name
            self._print(msg)
            return 1

        # if datapkg distribution use it first
        datapkgs  = [ r for r in pkg.resources if
            r['format'].startswith('datapkg') ]
        for dpkg in datapkgs:
            downloader = self.find_downloader(dpkg)
            if not downloader:
                continue

            self._print('Using datapkg distribution: %s' % dpkg )
            downloader.download(dpkg['url'], dest_path)
            # one datapkg is enough - nothing more needed
            return

        ## if not datapkg
        ## download first resource then query on all others

        self._print('Creating package metadata')
        # cribbed from datapkg/index/base.py:FileIndex
        import datapkg.distribution
        dist = datapkg.distribution.IniBasedDistribution(pkg)
        dist.write(dest_path)

        self._print('Downloading package resources ...')
        resource = pkg.resources[0]
        ## HACK: only do this because we have not sorted out file downloader to
        ## have right interface yet
        downloader = self.find_downloader(pkg.resources[0])
        self._print('Downloading package resources: %s' % resource) 
        downloader.download(resource['url'], dest_path)

    def find_downloader(self, resource):
        format = resource['format']
        format_type = format.split('/')[0]
        if format_type in [ 'api', 'resource' ]:
            self._print('Unable to retrieve resources of type: %s' % format)
            return None
        elif resource['format'] in ['datapkg/hg', 'datapkg/git']:
            self._print('Unable to retrieve resources of type: %s' % format)
            return None
        else: # treat everything as a retrievable file ...
            return datapkg.util.Downloader()

        ## TODO: reinstate this
        ## TODO: ? move this out to module level for performance?
#         for entry_point in pkg_resources.iter_entry_points('datapkg.download'):
#             downloader_cls = entry_point.load()
#             downloader = downloader_cls()

