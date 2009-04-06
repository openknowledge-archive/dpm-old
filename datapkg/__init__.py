'''datapkg is a tool for distributing, discovering and installing knowledge and
data 'packages'.

Contents:
    1. Quickstart
    2. Tutorial

1. Quickstart
+++++++++++++

Create a new data package on disk using standard file layout:

    $ datapkg create MyNewDataPackage

Edit the metadata:

    $ vim MyNewDataPackage/setup.py

Add some data:

    $ cp mydata.csv MyNewDataPackage
    $ cp mydata.js MyNewDataPackage
    $ etc ...

Register in your local repository on on CKAN:

    $ datapkg repo init # if repo not already initialized
    $ datapkg register MyNewDataPackage
    $ # OR
    $ datapkg register --repository=http://ckan.net/api/rest/ --api-key=....  MyNewDataPackage

Check it has registered ok:

    $ datapkg info MyNewDataPackage
    $ # OR
    $ datapkg info --repository=http://ckan.net/api/rest/ MyNewDataPackage


2. Tutorial
+++++++++++

datapkg has two distinct uses:

    1. Finding, obtaining and accessing material made available *by* others.
    2. Assisting you to make material available *to* others.

NB: in what follows items prefixed with $ should be run on the command line.


Basic Concepts
==============

Before we begin it is useful to understand some basic datapkg concepts:

    1. A Package -- metadata plus some set of resources (code, data etc)
    2. A Distribution -- a Package serialized to a structure on disk or at a url

For managing packages datapkg uses:

    1. An Index: a list of package metadata (but not package resources)
    2. Repository: an index plus a place to store package resources (as well as
       other miscellaneous facilities such as caches, configuration files etc)

When you start off, the first thing you will do is create a local repository.


1. Obtaining Material
=====================

1.1 Set Up Your Local Repository
--------------------------------

First set up your local repository::

    $ datapkg init

This will create a .datapkg directory in your home directory along with various
files including a main configuration file (config.ini).

NB: you can choose any location you like for your repository by passing the
--repository option to the init command. If you do so you will need to pass
this option to all other commands that require use of the repository.

[Optional] Edit your configuration file::

    $ vi .datapkg/config.ini


1.2 Install Material
--------------------

Suppose you have downloaded an existing datapkg distribution to your local
filesystem at {path}. (If you don't have one available you can download a demo
distribution from: http://knowledgeforge.net/ckan/pkgdemo.egg). Then you can
get info about it by doing:

    $ datapkg info {path}

You can register (this will not install it!) the package in your local index by
doing::

    $ datapkg register {path}

Once you have registered a package with name {name} you can replace any {path}
with {name} in most actions, e.g. you can now do::

    $ datapkg info {name}

You can install a package in your local repository either from a distribution
or a registered package by doing::

    $ datapkg install {path-or-name}

NB: to install from a registered package the package will need to have a
download_url associated.

[NOT YET OPERATIONAL] You can also do this with non-datapkg material Install a
package directly from a url::

    $ datapkg install {url}

TODO: support for replacing path at any point with a url


1.3 Using Material
------------------

Whether you just have a distribution on disk or have installed a package you
can access this material from the command line by using the `dump` command::

    $ datapkg dump {path-or-name} {path-in-package}

For example, if you have installed the pkgdemo package from earlier you could
do:

    $ datapkg dump pkgdemo windhover.txt

Which should result in Gerald Manley Hopkin's "The Windhover" being printed
out (as this is the contents of windhover.txt).

To access the package from python code do:

    import datapkg
    datapkg.make_available('{name-or-path}')


1.4 Find Material
-----------------

Search for a package on CKAN::

    $ datapkg --repository=http://ckan.net/api/rest/ list

You can find out about a package on CKAN by doing::

    $ datapkg --repository=http://ckan.net/api/rest/ info {pkg-name}

[NOT YET OPERATIONAL]

Pull CKAN index in your local index


2. Making Your Material Available to Others
===========================================

2.1 Creating a package (distribution)
-------------------------------------

First a skeletal distribution on disk::

    $ datapkg create {pkg-name-or-path}

Take a look inside your newly created distribution directory. There should
be 3 files/directories:

  1. MANIFEST.in: this specifies what files/directories within the distribution
  directory should actually be included in the package.
    * For instructions on using the MANIFEST.in to specify what files to
      include see <http://docs.python.org/distutils/commandref.html#sdist-cmd>
  2. *.egg-info: this directory you can safely ignore (though don't delete it)
  3. setup.py: this files holds metadata about your package.

Generally the only file you should have to alter is setup.py. Open this up in
your favourite editor and then modify the various attributes to be as you would
like them.

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

The first step in either process is building/compiling the distribution into a
standard form. This is most easily done by installing the package in your local
repository:

    $ datapkg install {path-to-distribution}

[NOT YET FULLY IMPLEMENTED]

Once that is done you register the package on CKAN by doing::

    $ datapkg --repository=http://ckan.net/api/rest/ register {path}


3. For Developers
=================

The easiest thing (which also guarantees up-to-date-ness) is to look through
the unit tests in ./datapkg/tests/
'''
__version__ = '0.2'
__description__ = 'Data packaging system and utilities.'
__description_long__ = __doc__
__license__ = 'MIT'
__license_full__ = \
'''All material is licensed under the MIT License:

Copyright (c) 2005-2008, Open Knowledge Foundation

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

import os

# TODO: 2009-03-09 Remove this.
# def install(name):
#     from manager import PackageManager
#     mgr = PackageManager()
#     mgr.install(name)
# 
# def upload(path='.'):
#     fns = os.listdir('.')
#     if 'setup.py' not in fns:
#         msg = '%s does not look like a data package (no setup.py ...)' % path
#         raise Exception(msg)
#     # TODO: implement the rest of this
    

class DatapkgException(Exception):
    pass
