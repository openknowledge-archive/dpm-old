'''dpm is a python library and command line tool for working with `Data
Packages`_ and interacting with data hubs like CKAN_.

For more information visit the documentation at:
http://readthedocs.org/docs/dpm/

.. _Data Packages: http://wiki.ckan.net/Data_Packages
.. _CKAN: http://ckan.org/
'''
__version__ = '0.10'
__description__ = 'dpm (data package): data packaging system and utilities'
__license__ = 'MIT'
__license_full__ = \
'''All material is licensed under the MIT License:

Copyright (c) 2005-2011, Open Knowledge Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

class DatapkgException(Exception):
    pass

import dpm.config
CONFIG = dpm.config.load_config()

import dpm.spec
def load_index(spec_str, all_index=False):
    '''Load a :class:`dpm.index.Index` specified by
    :class:`dpm.spec.Spec` spec_str.
    
    :param spec_str: a :class:`package spec <dpm.spec.Spec>`.
    :param all_index: hack param to state that spec is all about index (no
        package name). 
    '''
    spec = dpm.spec.Spec.parse_spec(spec_str, all_index=all_index)
    index, path = spec.index_from_spec()
    return index


def load_package(spec_str):
    '''Load `Package` specified by :class:`package spec <dpm.spec.Spec>` `spec_str`.

    :param spec_str: a :class:`package spec <dpm.spec.Spec>`.
    :return: Package.
    '''
    spec = dpm.spec.Spec.parse_spec(spec_str)
    index, path = spec.index_from_spec()
    return index.get(path)

