'''datapkg is a tool for easily distributing knowledge and data by using the
'packaging' concept, which is well established in software distribution. Full
documentation can be found at: http://knowledgeforge.net/ckan/doc/datapkg/

Contents:
    1. Quickstart
    2. Tutorial

NB: in what follows items prefixed with $ should be run on the command line.


1. Quickstart
+++++++++++++

Obtaining a Package
===================

Search for a package in an Index e.g. on CKAN.net::

    # let's search for iso country/language codes data (iso 3166 ...)
    $ datapkg search ckan:// iso
    ...
    iso-3166-2-data -- Linked ISO 3166-2 Data
    ...

Get some information about one of them::

    $ datapkg info ckan://iso-3166-2-data

Let's install it (to the current directory)::

    $ datapkg install ckan://iso-3166-2-data .

This will download the Package 'iso-3166-2-data' together with its "Resources"
and unpack it into a directory named 'iso-3166-2-data'.

Note that, if you replace the ckan:// spec with a file:// spec, you can use
most of the commands for files on disk. For example, if you've downloaded a
data package to, say, /tmp/xyz you could do::

    $ datapkg info file:///tmp/xyz

See the help on indivdual commands for more information.


Creating and Registering a Package
==================================

Create a new data Package on disk using datapkg file layout::

    $ datapkg create MyNewDataPackage

Edit the Package's metadata::

    $ vim MyNewDataPackage/setup.py

Add some data to the Package::

    $ cp mydata.csv MyNewDataPackage
    $ cp mydata.js MyNewDataPackage
    $ etc ...

Register it on CKAN::

    # NB: to register on CKAN you'll need to have an api-key
    # This can either be stored in your config file (see datapkg init config)
    # Or you can set it with the --api-key option
    $ datapkg register MyNewDataPackage ckan://

Check it has registered ok::

    $ datapkg info ckan://mynewdatapkg

[Not Yet Functional]: uploading package distributions.


2. Tutorial
+++++++++++

datapkg has two distinct uses:

    1. Finding and obtaining data made available *by* others.
    2. Making material available *to* others.


Basic Concepts
==============

Before we begin it is useful to understand some basic datapkg concepts:

    1. A Package -- the 'package' of data.
    2. A Distribution -- a serialization of the Package and optionally the data
       too (code, database, a book etc) to some concretely addressable form.
       For example: file(s) on disk, an API at a specific url.

For managing Packages datapkg uses:

    1. A Registry: a list of Package metadata (but not Package payload data)
    2. Repository: a Registry plus associated storage for association
       Distributions.

To specify a package (or just an index/repository) we often use a 'package
spec' (often termed just 'spec'), which have the following form::

    # for CKAN
    ckan://{package-name}
    # on disk
    file://{package-or-index-path}
    # or even just
    {package-or-index-path}


1. Obtaining Material
=====================

1.1 [Optional] Set Up Configuration
-----------------------------------

You may want to alter the default configuration, for example to specify your
CKAN apikey. To do this, first set up your local config::

    $ datapkg init config

This will create a .datapkgrc file in your home directory. You can then edit
this with your favourite text editor.

1.2 Locating and Installing Material
------------------------------------

See Quickstart section above.


2. Making Your Material Available to Others
===========================================

2.1 Creating a package (distribution)
-------------------------------------

First a skeletal distribution on disk::

    $ datapkg create {pkg-name-or-path}

Take a look inside your newly created distribution directory. There should
be 1 file:

  1. metadata.txt. This is an ini-style file that contains metadata in the form
  of Key: Value.

Having sorted out the metadata you will actually want to add some material to
your package. You do this by simply copying material into the distribution
directory, e.g.::

    $ cd {my-new-package}
    $ cp {lots-of-my-data-files} .


2. Register your package
------------------------

Now you have created a package you will want to make it available.

You can either do this by registering it on a public registry such as CKAN or,
more simply, you can just upload it somewhere and point people to that
location.

Once that is done you register the package on CKAN by doing::

    $ datapkg register {path} ckan://


3. Installing your package
--------------------------

You can also install a distribution (only onto disk at the moment!)::

    $ datapkg install {package-spec} {file-spec}


3. For Developers
=================

The easiest thing (which also guarantees up-to-date-ness) is to look through
the unit tests in ./datapkg/tests/
'''
__version__ = '0.6'
__description__ = 'Data packaging system and utilities.'
__description_long__ = __doc__
__license__ = 'MIT'
__license_full__ = \
'''All material is licensed under the MIT License:

Copyright (c) 2005-2010, Open Knowledge Foundation

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


import datapkg.spec
def load_index(spec_str, all_index=False, config=None):
    '''Load a `datapkg.index.Index` specified by spec string.
    
    @param all_index: hack param to state that spec is all about index (no
        package name). 
    @param config: config information
    '''
    spec = datapkg.spec.Spec.parse_spec(spec_str, all_index=all_index)
    index, path = spec.index_from_spec(config=config)
    return index


def load_package(spec_str):
    '''Load `Package` specified by `spec_str`.
    '''
    spec = datapkg.spec.Spec.parse_spec(spec_str)
    index, path = spec.index_from_spec()
    return index.get(path)

