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

import os
from os import path


import re
import json
import time

sys.path.insert(1,r'C:\Program Files\Dymola 2021x\Modelica\Library\python_interface\dymola.egg')
from dymola.dymola_interface import DymolaInterface
from dymola.dymola_exception import DymolaException

from multiprocessing import Process, ProcessError, Queue
from multiprocessing.managers import BaseManager

sys.path.insert(1,path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\__script__'))
import tools

###############################################################################
#                         CLASS DymolaSimulation                              #
###############################################################################

class DymolaSimulation(object):
    """
    Aim: Organize and automate the call of dymola python interface methods
    
    Author: H13483 - Braure Pierre (intern)
    """
    
    def __init__(self,libs,dymola_egg,dymola_launcher):
        """
        Instantiate the class.

        Parameters
        ----------

        libs : list
            List of libraries to be loaded (path to the package.mo file to be loaded)
        dymola_egg : str
            Path to the dymola_egg on your machine
        dymola_launcher : str
            Path to the dymola launcher (e.g. dymola.sh)
        """
        
        # self.parameters initialisation
        self.model_name = None
        self.model_path = None

        # Instantiate the Dymola interface and start Dymola
        try:
            self.dymola = DymolaInterface(dymolapath=dymola_launcher)
            print("dymola interface object created..")
        except DymolaException as err:
            print(f'__init__ -> error : {err}')

        # Load Modelica Libraries
        try:
            for library in libs :
                self.dymola.openModel(library)
                print(f'{library} load...\n')
        except DymolaException as err:
            print(f'__init__ -> error : {err}')
        
###############################################################################
#                                SETTERS                                      #
###############################################################################

    def set_model_path(self, model_path):
        self.model_path = model_path
    
    def set_model_name(self, model_name):
        self.model_name = model_name
    
    def set_wdir(self, wdir='.'):
        self.wdir = wdir

###############################################################################
#                                  GETTERS                                    #
###############################################################################

    def get_model_name(self):
        if not self.model_name:
            print("model_name unset.. please set model_name using the corresponding setters")
            return None
        
        return self.model_name

    def get_model_path(self):
        if not self.model_path:
            print("model_path unset.. please set model_path using the corresponding setters")
            return None
        
        return self.model_path

     
    def get_class_name(self):
        if not self.model_path:
            print("model_path unset.. please set model_path using the corresponding setters")
            return None

        # Last occurence of substring index research 
        main_string = path.join(repo_path,r'devtest_thermosyspro\ThermoSysPro')
        sub_string = "ThermoSysPro"
        last_index = main_string.rfind(sub_string)
        
        # refomarting string
        tmp = self.model_path[last_index:-3].replace('/','.')
        tmp = tmp.replace('\\','.')
        
        return tmp
    
    # (in development)
    # def get_timeout_relative(self):
    #     if not self.number_equation:
    #         self.gen_number_equation()
    #     if not self.gen_timerDico():
    #         self.gen_timerDico()
            
    #     sim_time = sum([value for value in timerDico.keys()])
        
    #     return 
    
###############################################################################
#                               GENERATORS                                    #
###############################################################################

    def gen_warningsDico(self, call):
        os.chdir(path.join(path.join(repo_path,f'devtest_thermosyspro\\Dev_TestSuite\\data\\{call}_results'), f'{self.model_name}'))
        frequentwarningList = ['Conflicting start values', 'The following parameters with fixed = false also have a binding', \
                            'Some variables are iteration variables of the initialization problem: but they are not given any explicit start values. Zero will be used.', \
                                'Others']
            
        warningsDico_keyList = [f'{call[0:3]}. w1', f'{call[0:3]}. w2', f'{call[0:3]}. w3', f'{call[0:3]}. others', f'{call[0:3]}. total']
        warnings = ''
        warningsList = []
        self.warningsDico = {warningsDico_keyList[i] : False for i in range(len(warningsDico_keyList))}
        self.warningsDico[f'{call[0:3]}. total'] = 0
        
        # Prints
        # print(f"dymola_simumlation_multiprocessing.py main -> warningsDico -> {self.warningsDico}")
        
        try:
            f = open('./lastlog.txt', 'r')
            for line in f:
                if "Warning:" in line and "WARNINGS have been issued" not in line:
                    
                    # Prints
                    # print(line, end='')
                    
                    warningsList.append(line)
                    warnings += line
                    
            f.close()
            
            # Prints
            # print(f"dymola_simumlation.py main -> warnings -> {warnings}")
            # print(f"dymola_simumlation.py main -> warningsList -> {warningsList}")
            
            if warnings:
                self.warningsDico = {warningsDico_keyList[i] : frequentwarningList[i] in warnings for i in range(len(frequentwarningList))}
                for i in range(len(warningsList)):
                    if warningsList[i] not in frequentwarningList:
                        self.warningsDico[f'{call[0:3]}. others'] = True
                self.warningsDico[f'{call[0:3]}. total'] = len(warningsList)
                
                # Prints
                # print(f"dymola_simumlation.py main -> warningsDico -> {self.warningsDico}")
                
                return True
            
            else:
                return False
            
        except OSError as err:
            print(f' gen_warningsDico -> error : {err}')
            return None
        
    def gen_timerDico(self):
        """
        
    
        Returns
        -------
        None.
    
        """
        try:
            # Initialization
            self.timerDico = {}
            
            wdir = path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data\simulation_results')
            
            # Lines scrapping for "CPU-time" keyword
            lines = self.txtFileInfoExtract('dslog', wdir, "CPU-time")
            
            self.timerDico['stop time (T)'] = self.stop_time
            
            if lines:
                self.timerDico['initialization time'] =  tools.get_time(lines[2])
                self.timerDico['integration time'] =  tools.get_time(lines[0])
                
            else:
                self.timerDico['initialization time'] = 0
                self.timerDico['integration time'] = 0
                
            self.timerDico[f'No timeout'] = False
            
            return True
        
        except Exception as err:
            print(f"gen_timerDico -> error during timers collect... : {err}")
            return False

    def gen_number_equation(self, call):
        """
        
        Returns
        -------
        None.

        """
        wdir = path.join(repo_path,f'devtest_thermosyspro\\Dev_TestSuite\\data\\{call}_results')
        lines = self.txtFileInfoExtract('lastlog', wdir, "scalar equations")
        
        try:
            self.number_equation = tools.trouver_nombres(lines[0])[1]
        except Exception as err:
            print(f'gen_number_equation -> error : {err}')
            print('continue...')
        pass
     
###############################################################################
#                               MAIN METHODS                                  #
###############################################################################
    
    def txtFileInfoExtract(self, name, wdir, keyword):
        """
        

        Returns
        -------
        None.

        """
        os.chdir(path.join(wdir, f'{self.model_name}'))
        
        try:
            f = open(f'./{name}.txt', 'r')
            infosList = [str(line) for line in f if f"{keyword}" in line]
            f.close()
            
            # Prints
            # print(f"-- PRINT -- \ndymola_simumlation.py main -> infosList -> {infosList}")
            
            return infosList
            
        except OSError as err:
            print(f'txtFileInfoExtract -> OSError : {err}')
            return None
      
    def change_wdir(self):
        """
        
        Returns
        -------
        None.

        """
        if not self.wdir:
            print("wdir needed.. please set wdir using the corresponding setters")
            return None
        
        os.chdir(self.wdir)
        self.dymola.cd(self.wdir)
        pass
  
    def referencefileGeneration(self, log=0):
        """
        Run a simulation

        Parameters
        ----------
        log : int, default: 0 (no line)
            Number of (end) lines of the log to print
        xxxx_path : str
            Path to the xxxxxx file (~/A_FOLDER/model.mo)
        """

        if not self.wdir:
            print("wdir needed.. please set wdir using the corresponding setters")
            return None

        if not self.model_path:
            print("model_path needed.. please set model_path using the corresponding setters")
            return None

        if not self.model_name:
            print("model_name needed.. please set model_path using the corresponding setters")
            return None

        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py referencefileGeneration -> self.model_name -> {self.model_name}\n")
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py referencefileGeneration -> self.model_path -> {self.model_path}\n")
        
        # Initialization
        returnsDico = {}

        print('Reference file generation...')
        referenceFileDirectory = path.join(repo_path,r'devtest_thermosyspro/Dev_TestSuite/data/referencefile_results/{self.get_class_name()}')
        returnsDico['command_result'] = self.dymola.ExecuteCommand(f'ModelManagement.Check.checkLibrary(false, false, false, false, "{self.get_class_name()}", generateReference=true, referenceFileDirectory={referenceFileDirectory}")')

        
        # Log saving
        lastlog = self.dymola.getLastErrorLog()
        if lastlog:
            try:
                f = open("lastlog.txt", "w")
                f.write(lastlog)
                f.close()
            except OSError as err:
                print(f'referencefileGeneration -> OSError : {err}')
                
        # Checking for referencefile generation resutls
        try:
            f = open("dslog.txt", "r")
            lines = f.readlines()
            f.close()
            if "SUCCESSFUL" in lines[-1]:
                returnsDico['ref_gen_result'] = True
            else:
                returnsDico['ref_gen_result'] = False
        
        except OSError as err:
            print(f'referencefileGeneration -> OSError : {err}')
            returnsDico['ref_gen_result'] = False
        
        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py referencefileGeneration -> returnsDico -> {returnsDico}\n")
        
        # Returns
        return returnsDico
    
    def severalReferencefileGeneration(self, model4simu):
        
        # Init
        iter = 0
        referencefileResultsDico = {'results' : {}, 'timers' : {}, 'warnings' : {}}
        referencefileGeneration_resultsDico = {}
        
        for dir_path, modelsubList in model4simu.items():
            for model in modelsubList:
                iter += 1
                
                model_name = model[:-3]  # model[:-3] for getiing off the ".mo" suffixe
                
                # Prints
                print("\nMODEL :", f'{model_name} ', f'({iter}/{str(sum([len(modelsubList) for dirpath, modelsubList in model4simu.items()]))})')
           
                
                # Directories Management
                try:
                    os.mkdir(f'{model_name}')
                except OSError as err:
                    print(f'severalReferencefileGeneration -> OSError : {err}')
                    print('still progress..')
                    continue

                wdir = os.path.join(os.getcwd(), f'{model_name}')
                

                
                # Settings
                self.set_model_name(model_name)
                self.set_model_path(os.path.join(dir_path, model))
                self.set_wdir(wdir)
                self.change_wdir()
                
                # Run of the model
                referencefileGeneration_resultsDico[f'{self.get_class_name()}'] = self.referencefileGeneration()
                referencefileResultsDico['results'][f'{self.get_class_name()}'] = referencefileGeneration_resultsDico[f'{self.get_class_name()}']['ref_gen_result']
                
                os.chdir('..')
            
        # Writting complete results in a .txt
        try:
            with open('referencefileGeneration_results.txt', 'w') as file:
                file.write(json.dumps(referencefileGeneration_resultsDico)) # use `json.loads` to do the reverse
                file.close()
        except Exception as err:
            print(f'severalReferencefileGeneration -> Error : {err}')
        
        # Closing the Dymola Instance    
        self.close()
        
        return referencefileResultsDico  
  
    def check(self, log=0):
        """
        Run a simulation

        Parameters
        ----------
        log : int, default: 0 (no line)
            Number of (end) lines of the log to print
        xxxx_path : str
            Path to the xxxxxx file (~/A_FOLDER/model.mo)
        """

        if not self.wdir:
            print("wdir needed.. please set wdir using the corresponding setters")
            return None

        if not self.model_path:
            print("model_path needed.. please set model_path using the corresponding setters")
            return None

        if not self.model_name:
            print("model_name needed.. please set model_path using the corresponding setters")
            return None

        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py check -> self.model_name -> {self.model_name}\n")
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py check -> self.model_path -> {self.model_path}\n")

        print("model checking...")
        result = self.dymola.checkModel(self.get_class_name())

        print(f'Check: {result}\n')
        
        # Log saving
        lastlog = self.dymola.getLastErrorLog()
        try:
            f = open("lastlog.txt", "w")
            f.write(lastlog)
            f.close()
        except OSError as err:
            print(f'check -> OSError : {err}')
        
        # Returns
        if not result:
            return False
        return True
    
    def severalCheck(self, model4simu):
        
        iter = 0
        checkResultsDico = {'results' : {}, 'timers' : {}, 'warnings' : {}}
        
        for dir_path, modelsubList in model4simu.items():
            for model in modelsubList:
                iter += 1
                
                model_name = model[:-3]  # model[:-3] for getiing off the ".mo" suffixe
                
                # Prints
                print("\nMODEL :", f'{model_name} ', f'({iter}/{str(sum([len(modelsubList) for dirpath, modelsubList in model4simu.items()]))})')
           
                
                # Directories Management
                try:
                    os.mkdir(f'{model_name}')
                except OSError as err:
                    print(f'severalCheck -> OSError : {err}')
                    print('still progress..')
                    continue

                wdir = os.path.join(os.getcwd(), f'{model_name}')
                
                # Settings
                self.set_model_name(model_name)
                self.set_model_path(os.path.join(dir_path, model))
                self.set_wdir(wdir)
                self.change_wdir()
                
                # Run of the model
                check_result = self.check()
                checkResultsDico['results'][f'{self.get_class_name()}'] = check_result
                
                os.chdir('..')
            
        # Closing the Dymola Instance    
        self.close()
        
        return checkResultsDico

    def translate(self, log=0):
        """
        Run a simulation

        Parameters
        ----------
        log : int, default: 0 (no line)
            Number of (end) lines of the log to print
        xxxx_path : str
            Path to the xxxxxx file (~/A_FOLDER/model.mo)
        """

        if not self.wdir:
            print("wdir needed.. please set wdir using the corresponding setters")
            return None

        if not self.model_path:
            print("model_path needed.. please set model_path using the corresponding setters")
            return None

        if not self.model_name:
            print("model_name needed.. please set model_path using the corresponding setters")
            return None

        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py translate -> self.model_name -> {self.model_name}\n")
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py translate -> self.model_path -> {self.model_path}\n")
        
        print("model translation...")
        start_time = time.time()
        result = self.dymola.translateModel(self.get_class_name())
        self.translation_time =  format(time.time() - start_time, '.3f')
        
        print(f'Translate: {result}\n')
        
        # Log saving
        lastlog = self.dymola.getLastErrorLog()
        try:
            f = open("lastlog.txt", "w")
            f.write(lastlog)
            f.close()
        except OSError as err:
            print(f'translate -> OSError : {err}')
        
        # Returns
        if not result:
            return False
        return True
        
    def severalTranslate(self, model4simu):

        iter = 0
        translateResultsDico = {'results' : {}, 'timers' : {}, 'warnings' : {}}

        for dir_path, modelsubList in model4simu.items():
            for model in modelsubList:
                iter += 1

                model_name = model[:-3]  # model[:-3] for getiing off the ".mo" suffixe

                # Prints
                print("\nMODEL :", f'{model_name} ',
                      f'({iter}/{str(sum([len(modelsubList) for dirpath, modelsubList in model4simu.items()]))})')
                
                # Directories Management
                try:
                    os.mkdir(f'{model_name}')
                except OSError as err:
                    print(f'severalTranslate -> OSError : {err}')
                    print('still progress..')
                    continue
                
                wdir = os.path.join(os.getcwd(), f'{model_name}')

                # Settings
                self.set_model_name(model_name)
                self.set_model_path(os.path.join(dir_path, model))
                self.set_wdir(wdir)
                self.change_wdir()

                # Run of the model
                translate_result = self.translate()
                translateResultsDico['results'][f'{self.get_class_name()}'] = translate_result
                
                # Generation
                self.gen_number_equation(call='translate')
                isWarning = self.gen_warningsDico(call='translate') # Also checking for translation warnings
                
                # if isWarning: # Not usefull for now
                translateResultsDico['warnings'][f'{self.get_class_name()}'] = self.warningsDico
                translateResultsDico['timers'][f'{self.get_class_name()}'] = {'translation time' : self.translation_time}
                
                # Prints
                # print(f"-- PRINT -- \ndymola_simulation.py severalTranslate -> number_equation -> {self.number_equation}\n")
                
                os.chdir('..')

        # Closing the Dymola Instance
        self.close()

        return translateResultsDico
        
    def simulate(self, log=0):
        """
        Run a simulation

        Parameters
        ----------
        log : int, default: 0 (no line)
            Number of (end) lines of the log to print
        xxxx_path : str
            Path to the xxxxxx file (~/A_FOLDER/model.mo)
        """
    
        
        if not self.wdir:
            print("wdir needed.. please set wdir using the corresponding setters")
            return None
        
        if not self.model_path:
            print("model_path needed.. please set model_path using the corresponding setters")
            return None
        
        if not self.model_name:
            print("model_name needed.. please set model_path using the corresponding setters")
            return None
        
        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py simulate -> self.model_name -> {self.model_name}\n")
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py simulate -> self.model_path -> {self.model_path}\n")
        
        # Initializaion
        try:
            self.class_text = self.dymola.getClassText(self.get_class_name(), includeAnnotations=True)[0]
            self.stop_time = int(re.findall(r'StopTime=(\d+)', self.class_text)[0])
        except Exception as err:
            self.stop_time = 1.0
            print(f'simulate -> error during StopTime collect : {err}\nStopTime will be set with T = 1')
            
        # Prints
        # print(f"-- PRINT -- \ndymola_simulation_multiprocessing.py simulate -> self.stop_time -> {self.stop_time}\n") 
        
        print("model simulation...")
        result = self.dymola.simulateModel(self.get_class_name(), resultFile=f'{self.model_name}')
                
        print(f'Simulation: {result}\n')
                
        # Log saving
        lastlog = self.dymola.getLastErrorLog()
        try:
            f = open("lastlog.txt", "w")
            f.write(lastlog)
            f.close()
        except OSError as err:
            print(f'simulate -> OSError : {err}')
        
        # Returns
        return result
 
    def severalSimulation(self, model4simu):
        iter = 0
        simResultsDico = {'results' : {}, 'timers' : {}, 'warnings' : {}}
        
        for dir_path, modelsubList in model4simu.items():
            for model in modelsubList:
                iter += 1
                
                model_name = model[:-3]  # model[:-3] for getiing off the ".mo" suffixe
                
                # Prints
                print("\nMODEL :", f'{model_name} ', f'({iter}/{str(sum([len(modelsubList) for dirpath, modelsubList in model4simu.items()]))})')
           
                
                # Directories Management
                try:
                    os.mkdir(f'{model_name}')
                except OSError as err:
                    print(f'severalSimulation -> OSError : {err}')
                    print('still progress..')
                    continue

                wdir = os.path.join(os.getcwd(), f'{model_name}')
                
                # Settings
                self.set_model_name(model_name)
                self.set_model_path(os.path.join(dir_path, model))
                self.set_wdir(wdir)
                self.change_wdir()
                              
                # Run of the model
                sim_result = self.simulate()
                simResultsDico['results'][f'{self.get_class_name()}'] = sim_result
                
                # Generation
                self.gen_number_equation(call='simulation')
                isWarning = self.gen_warningsDico(call='simulation') # Also checking for warnings

                # if isWarning: # Not usefull for now
                simResultsDico['warnings'][f'{self.get_class_name()}'] = self.warningsDico
            
                
                isTimerDico = self.gen_timerDico()
                
                # Prints
                # print(f"-- PRINT -- \ndymola_simulation.py severalSimulation -> timerDico -> {self.timerDico}\n")
                
                if isTimerDico:
                    simResultsDico['timers'][f'{self.get_class_name()}'] = self.timerDico
                
                os.chdir('..')
                
        # Closing the Dymola Instance    
        self.close()
        
        return simResultsDico

    def close(self) :
        """
        Terminate the Dymola session
        """
        if self.dymola is not None:
            self.dymola.close()
            self.dymola = None
            print("dymola session close!\n")
            
###############################################################################
#                                   MAIN                                      #
###############################################################################

if __name__ == '__main__':
    print('main : dymola_simulation')
    
    #from general_modules.generate_help_files import create_help_file
    
    #help_file_path = path.join(getcwd(),pardir,pardir,'Help','modelica_libraries','help_automatic_simulation.txt')
    #list_objects = [Automatic_Simulation]
    
    #create_help_file(help_file_path,list_objects)