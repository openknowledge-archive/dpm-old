=======
History
=======

v0.3 ????
=========

  * Distribution objects for writing and reading packages to disk

    * existing code refactored to PythonDistribution and new
      IniBasedDistribution implementation

  * Improved approach for configuration with config stored in a dedicated ini
    file
  * Create new Index object SimpleIndex
  * Significantly rework package metadata and additional attributes (author,
    maintainer, extras etc)
  * Improved, sphinx-built docs (http://knowledgeforge.net/ckan/doc/datapkg/)


v0.2 2009-03-18
===============

  * Completely refactor CLI making it better documented and easier to use
  * Support for 'flat' package structure on disk
  * Improve creation of on disk package (MANIFEST.in etc)
  * CKAN integration fully functional
  * Almost all commands now functioning *and* tested


v0.1 2008-12-15
===============

  * Manual much improved 
  * CLI: info and dump commands working (r331)
  * Substantial improvements to interface to setuptools and easy_install
    (pypkgtools)
  * First official released to PyPI
  * Several bugs fixed


v0.0.5 2008-07-15
=================

  * Start on manual
  * Core objects mostly working: Register, Repository, Package
  * Integration with CKAN (not tested)
  * Lots of tests
  * Basic functions but a way to go for proper upload/download cycle
  

2007-06-20: Project Started
===========================

