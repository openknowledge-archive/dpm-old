Installation
============

1. Install python: http://www.python.org/

2. Install setuptools library (and (optional) virtualenv)

3. Install dpm
   
   Using setuptool's easy_install::

      $ easy_install dpm
    
   Or to install with pip (http://pypi.python.org/pypi/pip)::

      $ pip install dpm

   If you want it in a nice insulated virtualenv do instead::

      # set up virtualenv
      $ virtualenv your_virtual_env

      # EITHER (with easy_install)
      $ . your_virtual_env/bin/activate
      $ easy_install dpm

      # OR (with pip) 
      $ pip -E your_virtual_env install dpm

   NB: if you wish to install from source dpm's git repository is
   here: https://github.com/okfn/dpm

4. Extras (e.g. upload capabilities).
   
   If you want to use the upload capabilities you will need to install the OFS library::

      $ easy_install ofs
      # or
      $ pip install ofs

   You can also install plugins - see the project's home page for a current list.

5. Take a look at the manual::

    $ dpm man

