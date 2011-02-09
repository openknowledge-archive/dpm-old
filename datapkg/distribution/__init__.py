'''A `Distribution` is a serialization of a `Package` to disk.
''' 
import os
import pkg_resources

from datapkg import DatapkgException
from datapkg.package import Package
import datapkg.metadata as M
from base import DistributionBase
from python import PythonDistribution
from jsondist import JsonDistribution

def get_distribution(distribution_name):
    '''Get Distribution class corresponding to the provided `distribution_name`.

    :param distribution_name: distribution name as specified by entry point name (setup.py
        entry_points) used to specify this distribution.
    '''
    # TODO: could speed this up by caching a dictionary of Index classes at
    # module level
    for entry_point in pkg_resources.iter_entry_points('datapkg.distribution'):
        if entry_point.name == distribution_name:
            cls = entry_point.load()
            return cls

def default_distribution():
    return get_distribution('json')

def load(path):
    '''Load distribution at path.
    
    Cycle through all available distribution types trying to load using each on
    in turn return first one which works.
    '''
    errors = []
    for entry_point in pkg_resources.iter_entry_points('datapkg.distribution'):
        klass = entry_point.load()
        try:
            dist = klass.load(path)
            return dist
        except Exception, inst:
            errors.append(str(inst))
    msg = 'Failed to load distribution from %s\n%s' % (path, errors)
    raise DatapkgException(msg)


