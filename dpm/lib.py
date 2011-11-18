"""
This is dpm library. It wraps all dpm functionalities inside Python functions.
For use it, import dpm.lib.
"""
import dpm
import dpm.spec
import dpm.index
import dpm.download
import dpm.config
import dpm.package
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

#
def get_config(section=None, option=None):
    """Return dpm configuration objects.

    :param section:
        the name of the section in the ini file, e.g. "index:ckan".
            - May be omitted only when no other parameters are provided
            - Must be omitted elsewhere
    :type section: str

    :param option:
        the name of the option to be retrieved from the section of the ini file, e.g. 'ckan.api_key'
            - Can be omitted if a section is provided
            - Must be omitted if no section is provided
    :type option: str


    :return:
        [str, str, .., str] --  The section names of the ini file, when no section and no option are provided
                                --  e.g. ['dpm', 'index:ckan', 'index:db', 'upload:ckan']
        [str, str, .., str] -- The option names of the ini file for a given section
                                -- e.g.['ckan.url', 'ckan.api_key']
        [str] -- The option value if a valid section and a valid option name are given.
                                -- e.g. ['http://thedatahub.org/api/']
    """
    if not section and not option:
        return dpm.CONFIG.sections()
    elif section and not option:
        return dpm.CONFIG.options(section)
    elif section and option:
        return dpm.CONFIG.get(section, option)
    else:
        raise ValueError("Please provide no parameters OR just section OR both section and option")


def set_config(section, option, value=None):
    """Set a dpm configuration value. If section or option are not already in the config, creates them.

    :param section:
        the name of the section in the ini file, e.g. "index:ckan".
    :type section: str

    :param option:
        the name of the option to be retrieved from the section of the ini file, e.g. 'ckan.api_key'
    :type option: str

    :param value:
        the new value for the option. If None, it sets the value as an empty string ''
    :type option: str


    :return:
        str -- The new option value
    """
    if section not in get_config():
        dpm.CONFIG.add_section(section)
    if not value:
        value = ""
    dpm.CONFIG.set(section, option, value)
    dpm.CONFIG.write(open(dpm.config.default_config_path, 'w'))
    dpm.CONFIG = dpm.config.load_config()
    return get_config(section, option)


def delete_config(section, option):
    """Delete a dpm configuration value. This function does not remove a dpm option, it only erases its current value.

    :param section:
        the name of the section in the ini file, e.g. "index:ckan".
    :type section: str

    :param option:
        the name of the option to be retrieved from the section of the ini file, e.g. 'ckan.api_key'
    :type option: str

    :return:
        str -- The new option value. That is, an empty string.
    """
    return set_config(section, option, "")


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
    pkg_downloader = dpm.download.PackageDownloader(verbose=True)

    filterfunc = None

    index, path = index_from_spec(package_spec)
    package = index.get(path)

    os_destination_path = os.path.join(destination_path, package.name)
    pkg_downloader.download(package, os_destination_path, filterfunc)

def load(package_path):
    '''Load a :py:class:`Package <dpm.package.Package>` stored at path

    :param package_path: The local Package path, e.g. /home/user/packages/iso-codes
    :type package_path: str

    :return: :py:class:`Package <dpm.package.Package>` -- The corresponding Package object
    '''
    #TODO: when this issue (https://github.com/okfn/dpm/issues/28) closes, update this function
    spec_str = "file://" + package_path
    spec = dpm.spec.Spec.parse_spec(spec_str)
    index, path = spec.index_from_spec()
    package = index.get(path)
    return package



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
        - (:py:class:`Metadata <dpm.metadata.Metadata>`, :py:class:`Manifest <dpm.package.Manifest>`) -- on success
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
    #TODO: will be like this one day, it does not work right now.
    #return search(index_spec, "")


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


def init(path, package_name):
    """Creates a new empty package

    :param path:
        - A local path where the package will be inited.
        - The path *must not* include the package name as final directory destination, e.g. "/tmp/packages/"
    :type path: str

    :param package_name:
            - The name of the package that will be inited
    :type package_name: str

    :return:
        - :py:class:`Package <dpm.package.Package>` -- The new Package object stored at package_path
    """
    package_path = os.path.join(path, package_name)
    return dpm.package.Package.create_on_disk(package_path)


def save(package):
    """Save Package changes to disk. The package _must_ already exist on disk. That is, it must be created with dpm.lib.init before.

    :param package:
        - The package that will be updated on disk
    :type package: :py:class:`Package <dpm.package.Package>`

    :return:
        - :py:class:`Package <dpm.package.Package>` -- The Package object stored at package_path
    """
    try:
        dpm.load_package("file://" + package.installed_path)
    except (IOError, TypeError):
        raise ValueError(
            "No valid installation path at " + str(package.installed_path) + ". Have you inited the package before?")

    package.dist.write(package.installed_path)
    package.name = os.path.basename(package.installed_path)
    return package


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

