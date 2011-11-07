"""
This is dpm library. It wraps all dpm functionalities inside Python functions.
For use it, import dpm.lib.
"""
import dpm
import dpm.spec
import dpm.index
import dpm.download
import dpm.config
import ckanclient
import os

def index_from_spec(spec_str, all_index=False):
    """Construct a dpm Index, given a spec string.

    :param spec_str:
        a string in the form of **<scheme>://<package name>**, where
            - **<scheme>** identifies the type of index to be used
            - **<package name>** identifies the name of the package.
            - Example: *ckan://iso-codes*
    :type spec_str: str
    
    :param all_index:
        this spec_str is just an index (useful for file specs)
    :type all_index:
        bool

    :return:
        (:py:class:`Index <dpm.index.base.IndexBase>`, str) -- str represents the Package (its name)

    :see:
        - :py:meth:`dpm.spec.Spec.parse_spec`
        - :py:func:`dpm.spec.index_from_spec`
    """
    spec = dpm.spec.Spec.parse_spec(spec_str, all_index=all_index)
    return spec.index_from_spec()

def get_config():
    """Return dpm configuration object

    :return:
        :py:class:`Config <dpm.config.Config>` -- The current configuration object
        
    :see:
        - :py:mod:`dpm.config`
    """
    return dpm.CONFIG

def get_package(package_spec):
    """Return `Package <dpm.index.package.Package>` given its Spec

    :param package_spec:
        a string in the form of **<scheme>://<package name>**, where
            - **<scheme>** identifies the type of index to be used
            - **<package name>** identifies the name of the package.
            - Example: *ckan://iso-codes*
            - Example: *file:///home/user/packages/useful-package*
    :type spec_str: str
    
    :return:
        :py:class:`Package <dpm.package.Package>` -- The Package object
    """
    package_index, package_name = index_from_spec(package_spec)
    return package_index.get(package_name)

def download(package_spec, destination_path):
    """Download a `Package <dpm.index.package.Package>` and the connected Resources

    :param package_spec:
        a string in the form of **<scheme>://<package name>**, where
            - **<scheme>** identifies the type of index to be used
            - **<package name>** identifies the name of the package.
            - Example: *ckan://iso-codes*
    :type spec_str: str

    :param destination_path:
        the directory in which to save the package
    :type destination_path: str

    :see:
        - :py:class:`dpm.download.PackageDownloader`
    """
    #TODO filter_resources and filterfunc
    #TODO add return values?

    pkg_downloader = dpm.download.PackageDownloader(verbose=True)

    filterfunc = None

    index, path = index_from_spec(package_spec)
    package = index.get(path)

    os_destination_path = os.path.join(destination_path, package.name)
    pkg_downloader.download(package, os_destination_path, filterfunc)


def info(package_spec_or_obj):
    """Retrieve information about a :py:class:`Package <dpm.index.package.Package>`

    :param package_spec_or_obj:
        - a string in the form of **<scheme>://<package name>**, where
            - **<scheme>** identifies the type of index to be used
            - **<package name>** identifies the name of the package.
            - Example: *ckan://iso-codes*
        - the :py:class:`Package <dpm.index.package.Package>` object
    :type package_spec: str or :py:class:`dpm.index.package.Package`

    :return:
        - (:py:class:`Metadata <dpm.metadata.Metadata>`,:py:class:`Manifest <dpm.package.Manifest>`) -- on success
        - None -- on un-success
    """
    if type(package_spec_or_obj) == str:
        index, path = index_from_spec(package_spec_or_obj)
        package = index.get(path)
    else: # assume package_spec_or_obj is of type Package, will check for it next
        package = package_spec_or_obj

    if not type(package) == dpm.package.Package:
        return None #TODO: raise an exception here?
    
    return (package.manifest, package.metadata)


def list(index_spec):
    """Return the `Packages <dpm.index.package.Package>` (not their resources!) pointed by an index
    
    :param index_spec:
        - a string in the form of **<scheme>://**, where
            - **<scheme>** identifies the type of index to be used
            - Example: *ckan://*
    :type index_spec: str

    :return:
        - [:py:class:`Package <dpm.package.Package>`] -- A list of Packages pointed by the Index
        - Actually, dpm lacks the case in which an exception occurs (see :py:meth:`dpm.index.Ckan.list`)
    """
    index, path = index_from_spec(index_spec, all_index=True)
    packages = index.list()
    return packages


def search(index_spec, query):
    """Search in the Packages pointed by an Index

    :param index_spec:
        - a string in the form of **<scheme>://**, where
            - **<scheme>** identifies the type of index to be used
            - Example: *ckan://*
    :type index_spec: str

    :param query:
        a string specifying the query to be executed.
        Ex: iso

    :return:
        - [:py:class:`Package <dpm.package.Package>`] -- A list of Packages pointed by the Index satisfying the query
        - [] -- on no results
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



def init():
    """Not yet implemented"""
    pass

def dump():
    """Not yet implemented"""
    pass

def setup():
    """Not yet implemented"""
    #TODO split it in 3 different methods
    pass

def register():
    """Not yet implemented"""
    pass

def update():
    """Not yet implemented"""
    pass

def upload():
    """Not yet implemented"""
    pass

