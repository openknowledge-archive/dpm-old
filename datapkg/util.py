import platform

# annoyingly there does not seem to be a single standard way to check you are
# on windows
def getstatusoutput(cmd):
    '''Wrap L{commands.getstatusoutput} so it works on Windows.'''
    os = platform.system()
    if  os == 'Windows':
        # from http://gizmodise.com/linux/?p=70 
        import os
        pipe = os.popen('\"' + cmd + '\" 2>&1', 'r')
        text = pipe.read()
        sts = pipe.close()
        if sts is None: sts = 0
        if text[-1:] == '\n': text = text[:-1]
        return sts, text
    else:
        import commands
        return commands.getstatusoutput(cmd)

