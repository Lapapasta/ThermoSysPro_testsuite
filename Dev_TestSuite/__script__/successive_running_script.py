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

sys.path.insert(1,path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\__class__'))
from io_management import IO_Management

sys.path.insert(1,path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\__class__'))
import check
import translate
import simulation
import referencefile_generation
import clean_all
import html_generation

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
        
    print('\n--- SUCCESSIVE RUNNING SCRIPT ---\n')
    
    os.chdir(path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite'))
    
    # Directories Management
    try:
        os.mkdir('data')
    except OSError as err:
        print(f'OSError : {err}')
        print('still progress..')
    
    # Main function call
    # clean_all.main()
    # check.main()
    # translate.main()
    # simulation.main()
    # referencefile_generation.main()
        
    # Csv file generation
    # IO_Manager = IO_Management()
    # IO_Manager.csvCompact()
    
    # HTML generation
    # html_generation.main()
    
    return 0
    
if __name__ == '__main__':
    main()

    