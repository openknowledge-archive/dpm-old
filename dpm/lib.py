__author__ = 'dgraziotin'
"""
This module holds what we hope will become the future standard library for dpm, to be used
by both the command line, the GUI and other projects.
APIs are documented in each function.
"""
import dpm
import dpm.spec
import dpm.index
import dpm.download
import dpm.config
import ckanclient
import os
import shutil

#TODO should we really export this functionality? can be useful.
def index_from_spec(spec_str, all_index=False):
    spec = dpm.spec.Spec.parse_spec(spec_str, all_index=all_index)
    return spec.index_from_spec()


def create():
    pass

def get_config():
    """
    Returns dpm configuration

    Return values:
    None if the configuration does not exist.
    a dpm.config.Config object on success
    """
    return dpm.CONFIG

def download(package_spec, destination_path): #still have to understand this: filter_resources=["*"]):
    """Download a Package and the connected Resources

    Keyword arguments:
    package_spec -- a string Spec in the form of <scheme>://<package name>, where:
                    <scheme> identifies the type of index to be used
                    <package name> identifies the name of the package
                    Ex: ckan://iso-codes
    destination_path -- a string specifying the directory in which to save the package


    Return values:
    True if the operation succeeds
    The actual dpm design does not let us to specify other values. Must fix this
    """
    #TODO better return values

    pkg_downloader = dpm.download.PackageDownloader(verbose=True)

    '''
    The following are typical dpm download usage

    # download the package specified by ckan://name to path-on-disk
    # selecting the resources to retrieve interactively
    download ckan://name path-on-disk

    # download all resources
    # Note need to quote *
    download ckan://name path-on-disk "*"

    # download only those resources that have format 'csv' (or 'CSV')
    download ckan://name path-on-disk csv

    # download only those resources that have format starting xml/
    download ckan://name path-on-disk xml/*

    # download only those resources that have a url starting http://abc (and any format)
    download ckan://name path-on-disk "*" http://abc*

    Just the first two work for me now, the other will be supported when I understand them.
    '''

    #TODO this will probably work someday
    '''
    print len(filter_resources)
    if len(filter_resources) == 1:
        formatpat = filter_resources[0]
        urlpat = "*"
    else:
        formatpat = filter_resources[0]
        urlpat = ' '.join(str(item) for item in filter_resources[1:])

    filterfunc = pkg_downloader.make_glob_filterfunc(
                formatpat,
                urlpat)
    '''

    filterfunc = None

    index, path = index_from_spec(package_spec)
    package = index.get(path)

    os_destination_path = os.path.join(destination_path, package.name)
    pkg_downloader.download(package, os_destination_path, filterfunc)
    return True


def info(package_spec, request_for='metadata'):
    #TODO: a better argument instead of request_for?
    """Retrieve info on Package

    Keyword arguments:
    package_spec -- either:
                    * a string Spec in the form of <scheme>://<package name>, where:
                    <scheme> identifies the type of index to be used
                    <package name> identifies the name of the package
                    Ex: ckan://iso-codes.
                    * an object of type Package
    request_for -- a string specifying what to retrieve. Up to know we let choose either for 'metadata'
                   or for 'manifest'. Default is 'manifest'


    Return values:
    The package Metadata (or the Manifest)
    None elsewhere
    """
    if type(package_spec) == str:
        index, path = index_from_spec(package_spec)
        package = index.get(path)
    else: # assume package_spec is of type Package, will check for it next
        package = package_spec

    if not type(package) == dpm.package.Package:
        return None
    if request_for == 'metadata':
        return package.metadata
    elif request_for == 'manifest':
        return package.manifest
    else: # fallback
        return package.metadata


def list(index_spec=""):
    """Returns the Packages (not the resources) pointed by an index

    Keyword arguments:
    index_spec -- a string in the form of <scheme>://, where <scheme> identifies the type of index to be used.
                  Ex: ckan://

    Return values:
    A list of Packages pointed by the Index
    Actually, dpm lacks the case in which an exception occurs (see dpm.index.ckan.py.list())
    """
    index, path = index_from_spec(index_spec, all_index=True)
    packages = index.list()
    return packages


def register():
    pass


def search(index_spec, query):
    """Search a Package

    Keyword arguments:
    index_spec -- a string in the form of <scheme>://, where <scheme> identifies the type of index to be used.
                  Ex: ckan://
    query -- a string specifying the query to be executed.
             Ex: iso

    Return values:
    A list of Package object if there are results
    An empty list elsewhere
    """
    spec_from = index_spec
    index, path = index_from_spec(spec_from)
    packages = []
    try:
        for package in index.search(query):
            packages.append(package)
    except ckanclient.CkanApiNotAuthorizedError:
        pass #TODO: just a workaround now
    return packages


def update():
    pass


