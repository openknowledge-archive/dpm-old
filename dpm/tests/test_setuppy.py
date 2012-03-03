import os

import dpm.util

def test_simple():
    cmd = 'python setup.py egg_info'
    status, output = dpm.util.getstatusoutput(cmd)
    assert not status, output

