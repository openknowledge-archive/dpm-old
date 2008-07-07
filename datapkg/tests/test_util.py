import platform

import datapkg.util

def test_getstatusoutput():
    exp = 'Python %s' % platform.python_version()
    cmd = 'python -V'
    status, output = datapkg.util.getstatusoutput(cmd)
    assert output == exp

