=============
Distributions
=============

A Distribution is a serialization of the Package and optionally the data too
(code, database, a book etc) to some concretely addressable form that can be
'distributed' (e.g. uploaded) or accessed (e.g. downloaded). For example:

  * file(s) on disk
  * an API at a specific url.


.. note::

    To the extent possible, we seek to reuse existing 'distribution' formats
    rather than invent our own.

Currently, we provide 2 types of basic file distributions:

  * Simple (Ini-Based) Distribution - DEFAULT
  * Python Distribution

It is also easy to extend datapkg to support new distribution types. See
Extending Datapkg.

Base Distribution
=================

.. autoclass:: datapkg.distribution.DistributionBase
  :members:

Simple Distribution
===================

.. autoclass:: datapkg.distribution.SimpleDistribution
  :members:

Python Distribution
===================

.. autoclass:: datapkg.distribution.PythonDistribution
  :members:

