'''A `Distribution` is a serialization of a `Package` to disk.
''' 
import os
import pkg_resources

from dpm import DatapkgException
from dpm.package import Package
import dpm.metadata as M
from base import DistributionBase
from jsondist import JsonDistribution

def get_distribution(distribution_name):
    '''Get Distribution class corresponding to the provided `distribution_name`.

    :param distribution_name: distribution name as specified by entry point name (setup.py
        entry_points) used to specify this distribution.
    '''
    for entry_point in pkg_resources.iter_entry_points('dpm.distribution'):
        if entry_point.name == distribution_name:
            cls = entry_point.load()
            return cls

def default_distribution():
    return get_distribution('json')

def load(path):
    errors = []
    klass = default_distribution()
    dist = klass.load(path)
    return dist

