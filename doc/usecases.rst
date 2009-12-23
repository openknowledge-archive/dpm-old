Use cases for datapkg
=====================

Consumer user role
------------------

 1. Install datapkg
 2. Search remote registry/repo for a package
 3. Download package on to local disk and unpack::

     $ datapkg get [url|name] [path]

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


