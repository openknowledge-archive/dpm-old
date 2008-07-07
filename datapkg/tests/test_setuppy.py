import os

import datapkg.util

def test_simple():
    cmd = 'python setup.py egg_info'
    status, output = datapkg.util.getstatusoutput(cmd)
    assert not status, output

