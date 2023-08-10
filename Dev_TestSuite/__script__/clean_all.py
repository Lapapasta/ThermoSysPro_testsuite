# -*- coding: utf-8 -*-
###############################################################################
#                                CONFIG.                                      #
###############################################################################

import sys, os
sys.path.insert(1,os.getcwd())
from config import *

###############################################################################
#                            LIBRARIES IMPORT                                 #
###############################################################################

from os import path
import shutil

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
    folder = path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try: # os.removedirs() better ?
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
if __name__ == '__main__':
    print('\n--- CLEANING SCRIPT ---\n')
    main()
    