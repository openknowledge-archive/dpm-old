Introduction
============

datapkg is a tool for distributing, discovering and installing knowledge and
data 'packages'.

For more information visit the documentation at:
http://knowledgeforge.net/ckan/doc/datapkg/


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

