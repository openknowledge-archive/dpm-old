Introduction
============

datapkg is a python library and command line tool for working with `Data
Packages`_ and interacting with data hubs like CKAN_.

For more information visit the documentation at:
http://packages.python.org/datapkg/

.. _Data Packages: http://wiki.ckan.net/Data_Package
.. _CKAN: http://ckan.org/

Installation
============

See doc/install.rst or the online documentation.


License
=======

See doc/license.rst


For Developers
==============

1. Building the documentation.

You need sphinx (python-sphinx) to do this. Now you can build the docs::

    python setup.py build_sphinx

2. Running tests. We suggest you use nose::

    nosetests datapkg/tests/
  
  To exclude tests depend on access to the internet::

    nosetests -a \!__external__ datapkg/tests

