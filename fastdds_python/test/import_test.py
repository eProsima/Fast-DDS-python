#!/usr/bin/python3

# Windows workaround (see https://bugs.python.org/issue46276)
import os
if os.name == 'nt':
    import win32api
    win32api.LoadLibrary('_fastdds_python.pyd')
    win32api.LoadLibrary('_test_completeWrapper.pyd')

import fastdds
import test_complete

print('Greetings from the Fast-DDS python wrapper')
