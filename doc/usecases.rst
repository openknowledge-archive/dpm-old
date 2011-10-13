=====================
Use cases for dpm
=====================

Use cases for DataPkg (or: reasons to use it in the first place)

These use cases are not necessarily all implemented but are a guide to what we
are *trying to do*. The first two were the two original use cases at the start
of the project (and were heavily inspired by debian).

1. Grabbing some data from an index
===================================

The steps involved::

    $ dpm index-add file:///....
    $ dpm update
    $ dpm search "military spending"

    some-id Military Spending 1890-1914
    some-id-2 Military Spending 1890-1914 (normalized)

    $ dpm install some-id
    ...
    $ dpm plot some-id

2. Get two different datasets and use them together
===================================================

What data?

  * Normalize data

    * Cross country and then convert to standard (e.g. US$, GBP)

      * Exchange rates
      * Cost of living

    * Changes across time and then do real present value

  * [Plot two different data sources again each other.]

    * [Government expenditure in different sectors?]

Example code::

    $ dpm install pkg-a
    $ dpm install pkg-b
    $ dpm create merged
      # manual merge
      # e.g. PPP, GDP
    $ dpm register my-merged-package


Getting data v2
===============

Revist basic discovery and usage of data from above.

  1. Install dpm
  2. Search remote registry/repo for a package
  3. Download package on to local disk and unpack::

     $ dpm get [url|name] [path]

   If specifying name (using a Registry) then:

     * get metadata from registry
     * locate the distribution URL

   Basic steps:

     * Discover at URL: targz/zip file, version controlled repo, URL page with links (ask user which one)
     * download the compressed distribution to temp dir (progress bar)
     * unpack it to destination path

   Future: maybe need to build/compile data

 4. Explore package


Publisher user role
-------------------

 1. Package a csv file
 2. Register the package to the remote repo.
 3. Upload the package distribution to the remote repo.


