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
from dymola_simulation_multiprocessing import DymolaSimulation

# Old one without process encapsulation
# from dymola_simulation import DymolaSimulation

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
    print('\n--- EXAMPLES SIMULATION ---\n')
    
    os.chdir(path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data'))
    
    # Directories Management
    try:
        os.mkdir('simulation_results')
    except OSError as err:
        print(f'OSError : {err}')
        print('still progress..')
    
    # Reception directories for simulation results
    os.chdir(os.path.join(path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data'),'simulation_results'))
    
    # Initialisation of the DymolaSimulation Instance
    DymolaInstance = DymolaSimulation(
    libs=[tsp_path],
    dymola_egg=dymola_egg,
    dymola_launcher=dymola_launcher
    )

    # IO_Management Part
    IO_Manager = IO_Management()
    IO_Manager.getModel(path.join(repo_path,r'devtest_thermosyspro\ThermoSysPro'), 'Examples')
    
    # Model number reduction for test
    # newmodel4simu = [values for values in IO_Manager.model4simu.values()][0][2:8]
    # IO_Manager.model4simu[path.join(repo_path,r'devtest_thermosyspro\ThermoSysPro\Examples\SimpleExamples')] = newmodel4simu
    
    # Models simulation
    simulationResultsDico = DymolaInstance.severalSimulation(IO_Manager.model4simu)

    # Simulation results reception
    IO_Manager.setParams(simulationResultsDico=simulationResultsDico)
    
    # print(f"-- PRINT -- \nsimulation.py main -> IO_Manager.paramsDico['simulationResultsDico'] -> {IO_Manager.paramsDico['simulationResultsDico']} \n")
   
    # Export simulation results into a .csv file
    if IO_Manager.paramsDico['simulationResultsDico']['results']:
         IO_Manager.csvCall(call='simulation')
    
    return 0

if __name__ == '__main__':
    main()
    sys.exit()
    
    
###############################################################################
#                                   ANNEXE                                    #
###############################################################################

# OTHERS
# Some prints
# print(f'-- PRINT -- \n{IO_Manager.model4simu.values()}')
# print(f'-- PRINT -- \n{IO_Manager.model4simu.keys()}')
# print(f'-- PRINT -- \n{[values for values in IO_Manager.model4simu.values()][subList_index]}')
# print(f'-- PRINT -- \n{[keys for keys in IO_Manager.model4simu.keys()][subList_index]}')

# Model for simulation number reduction (in developpement)
# subList_index = 1
# # model_index = 0 # non fonctionnel
# newmodel4simu = {f'{[keys for keys in IO_Manager.model4simu.keys()][subList_index]}' : [values for values in IO_Manager.model4simu.values()][subList_index]}
# # print(-- PRINT -- \nnewmodel4simu)
# IO_Manager.model4simu = newmodel4simu