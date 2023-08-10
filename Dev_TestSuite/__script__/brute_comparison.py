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

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
    print('--- COMPARISION TEST ---')
    os.chdir(path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data'))
    
    # Directories Management
    try:
        os.mkdir('results_compare')
    except OSError as err:
        print(f'OSError : {err}')
        print('still progress..')
        
    try:
        os.remove(path.join(repo_path,"devtest_thermosyspro/Dev_TestSuite/data/results_compare/" \
                   "results_compare.txt"))
    except:
        pass
    
    # Initialization
    wdir = path.join(repo_path,"devtest_thermosyspro/Dev_TestSuite/data/results_compare/")
    os.chdir(wdir)
    
    # IO_Manager Initialisation
    IO_Manager = IO_Management()
    
    # Directories path for reference model, actual model and comparison file
    ref_lib = path.join(repo_path,"devtest_thermosyspro/Dev_TestSuite/data/referencefile_results")
    act_lib = path.join(repo_path,"devtest_thermosyspro/Dev_TestSuite/data/simulation_results")
    csv_path = wdir + "results_compare.csv"
    
    
    IO_Manager.setParams(
        ref_lib = ref_lib,
        act_lib = act_lib,
        csv_path = csv_path
        )
    
    IO_Manager.comparisionTestSeveral()
    IO_Manager.csvSplit()
    
if __name__ == '__main__':
    main()
