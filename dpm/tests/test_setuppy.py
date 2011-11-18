import os

import dpm.util

def test_simple():
    cmd = 'python setup.py egg_info'
    status, output = dpm.util.getstatusoutput(cmd)
    #assert not status, output
    # there is output from that command (dgraziotin)
    assert not status and output

