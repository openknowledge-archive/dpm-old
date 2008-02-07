# datapkg.
__version__ = '0.1dev'
__description__ = 'Data packaging system and utilities.'
__description_long__ = ''
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

from package import Package, PackagePython
from manager import PackageManager

def create(name, base_path=''):
    '''Create a skeleton data package

    >>> import datapkg
    >>> os.chdir('/tmp')
    >>> pkg_name = 'my-random-name'
    >>> datapkg.create(pkg_name)
        ...
    '''
    cmd = 'paster create --template=datapkg '
    if base_path:
        cmd += '--output-dir %s ' % base_path
    cmd += name
    os.system(cmd)

from paste.script.templates import Template
class DataPkgTemplate(Template):
    _template_dir = 'templates/default_distribution'
    summary = 'DataPkg default distribution template'

def install(name):
    mgr = PackageManager()
    mgr.install(name)

def upload(path='.'):
    fns = os.listdir('.')
    if 'setup.py' not in fns:
        msg = '%s does not look like a data package (no setup.py ...)' % path
        raise Exception(msg)
    
