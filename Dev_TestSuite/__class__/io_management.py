# -*- coding: utf-8 -*-
###############################################################################
#                                CONFIG.                                      #
###############################################################################

import sys
sys.path.insert(1,r'C:\Users\H13483\Documents\devtest_thermosyspro\Dev_TestSuite\__script__')
from config import *

###############################################################################
#                            LIBRARIES IMPORT                                 #
###############################################################################

import os
from os import path, walk


import csv

# read the generated mat files values
from buildingspy.io.outputfile import Reader

# to retrive the model name, and then the time instants in the dictionary key
import operator

import pandas as pd

###############################################################################
#                                FUNCTION                                     #
###############################################################################

# add the corresponding headers for every column in the edited csv files
def add_header(pathname):
    length = []
    with open(pathname, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = ["Time", "Model Name"]
        data = [row for row in reader]
        
        # Prints
        # print(f'-- PRINT -- \nadd_header -> data -> {data}')
        
        for i in range(len(data)):
            length.append(len(data[i]))
        for j in range(0, int(max(length)) - 2, 4):
            header.append("Variable Name")
            header.append("Actual Values")
            header.append("Reference Values")
            header.append("Delta")
    with open(pathname, "w+", newline="") as csvfile:
        f = csv.writer(csvfile, delimiter=';')
        f.writerow(header)
        for row in data:
            f.writerow(row)
    pass

def resultscomparewrite_nonsense(model_name, keyword):
    with open('results_compare.txt','a') as txtfile:
        if keyword == 'key':
            txtfile.write(f" - {model_name} : Comparision test as no sense, different variables in models\n")
        elif keyword == 'times':
            txtfile.write(f" - {model_name} : Comparision test as no sense, different simulation's time intervals\n")
        txtfile.close()
        

###############################################################################
#                           CLASS IO_Management                               #
###############################################################################

class IO_Management(object):
    """
    Aim: Regroup the class interacting with outside data (.csv, .mo, .mat, etc..)
    
    Author: H13483 - Braure Pierre (intern)
    """
    
    def __init__(self):
        self.paramsDico = {}
        pass
    
    def comparisionTest(self, act_matvaluesDico, ref_matvaluesDico, model_name):
        Diff = None
        
        # Prints
        # print(f"-- PRINT -- \nio_management.py -> act_matvaluesDico.keys() -> {act_matvaluesDico.keys()}\n")
        # print(f"-- PRINT -- \nio_management.py -> ref_matvaluesDico.keys() -> {ref_matvaluesDico.keys()}\n")
        
        act_keyList = [key for key in act_matvaluesDico.keys()]
        ref_keyList = [key for key in ref_matvaluesDico.keys()]
        
        
        with open(self.paramsDico['csv_path'], 'a', newline="") as csvfile:
            f = csv.writer(csvfile, delimiter=';') 
            # Checking for model variables differences
            if not act_keyList == ref_keyList:
                resultscomparewrite_nonsense(model_name, 'key')
                print('return if not(act_matvaluesDico.keys() == ref_matvaluesDico.keys())')
                return Diff
            
            iter = -1
            while (Diff == None) & (iter < len(act_keyList) - 1):
                iter += 1
                # # Compare time intervals values (in development)
                # if (ref_matvaluesDico[key][0] == act_matvaluesDico[key][0]).all():
                #     resultscomparewrite_nonsense(model_name, 'times')
                #     continue
                    
                # Prints
                # print(f"-- PRINT -- \nio_management.py -> ref_matvaluesDico[act_keyList[{iter}]][1] -> {ref_matvaluesDico[act_keyList[iter]][1]}\n")
                
                # ref_matvaluesDico[key][1] corresponds to variable values
                # Compare variables values for each values
                if not (ref_matvaluesDico[act_keyList[iter]][1] == act_matvaluesDico[act_keyList[iter]][1]).all():
                    Diff = True
            
            # Verifying for Diff = None
            if not Diff:
                Diff = False
            
            if Diff:    
                for key in act_keyList:
                    for i in range(len(act_matvaluesDico[key][1])):
                        if act_matvaluesDico[key][1][i] != ref_matvaluesDico[key][1][i]:
                            delta = act_matvaluesDico[key][1][i] - ref_matvaluesDico[key][1][i]
                            data = [act_matvaluesDico[key][0][i], f'{model_name}', f'{key}', act_matvaluesDico[key][1][i], ref_matvaluesDico[key][1][i], delta]
                            # Writing in file
                            f.writerow(data)
        return Diff
           
    def comparisionTestSeveral(self):

        self.diff_num = 0
        self.csv_names = []
        dirnames = os.listdir(path=self.paramsDico['act_lib'])
        
        # Write in results_compare.txt
        with open('results_compare.txt','a') as txtfile:
            txtfile.write("###### COMPARISION TEST ######\n")
            txtfile.write("## Compare the simulation's results for each variables at each step time and warns for differences ## \n")
            txtfile.write(f" - Reference library path : {self.paramsDico['ref_lib']} \n")
            txtfile.write(f" - Tested library path : {self.paramsDico['act_lib']} \n")
            txtfile.write("\n##### MODELS UNDER TEST #####\n")
            for dirname in dirnames:
                if '.csv' not in dirname:
                    txtfile.write(f" - {dirname}\n")
            txtfile.write("\n##### RESULTS #####\n")
        txtfile.close()
        
        for dirname in dirnames:
            if '.csv' not in dirname:
                
                class_name = ''
                
                self.modelList = dirnames
                
                error_message = []
                model_name = dirname
                print(f'\nCurrent model : {model_name}\n')
                
                # Try to open the dslog.txt file
                try:
                    with open(f"{self.paramsDico['act_lib']}/{dirname}/dslog.txt",'r') as f:
                        text = f.readlines()
                        isdslog = True
                        f.close()
                        
                except FileNotFoundError as err:
                    isdslog = False
                    error_message.append(f'FileNotFoundError :  {err}')
                    error_message.append(f'\nComparison failed for {model_name}..')
    
                # Directories settings
                class_name = text[4][5:-13]
                mat_ref_model_name = class_name + '_ref'
                act_mat_dir = self.paramsDico['act_lib'] + "/" + model_name
                ref_mat_dir = self.paramsDico['ref_lib'] + "/" + class_name
                
                # Try to read of .mat files
                try:
                    act = Reader(act_mat_dir + "/" + model_name + ".mat", "dymola")
                    ismatfile_tested = True
                except FileNotFoundError as err:
                    ismatfile_tested = False
                    if error_message:
                        error_message[0] += f'\nFileNotFoundError : {err}'
                    else:
                        error_message.append(f'FileNotFoundError :  {err}')
                        error_message.append(f'\nComparison impossible for {model_name}..')
                        
                try:
                    ref = Reader(ref_mat_dir + "/" + mat_ref_model_name + ".mat", "dymola")
                    ismatfile_ref = True
                except FileNotFoundError as err:
                    ismatfile_ref = False
                    if error_message:
                        error_message[0] += f'\nFileNotFoundError : {err}'
                    else:
                        error_message.append(f'FileNotFoundError :  {err}')
                        error_message.append(f'\nComparison impossible for {model_name}..\n')
                    
                        
                if error_message:
                    # Write in results_compare.txt
                    with open('results_compare.txt','a') as txtfile:
                        txtfile.write(f" - {model_name} : Comparision impossible")
                        if not ismatfile_tested:
                            txtfile.write(" - tested model .mat file missing")
                        if not ismatfile_ref:
                            txtfile.write(" - ref model .mat file missing")
                        if not isdslog:
                            txtfile.write(" - tested model dslog.txt file missing") 
                        txtfile.write("\n")    
                    txtfile.close()
                    
                    # Prints
                    for err in error_message:
                        print(f'{err}')
                    continue
    
                act_matvaluesDico = self.get_matvaluesDico(act)
                ref_matvaluesDico = self.get_matvaluesDico(ref)
                
                print('call comparisionTest')
                Diff = self.comparisionTest(act_matvaluesDico, ref_matvaluesDico, model_name)   
                
                # Prints
                # print(f"-- PRINT -- \nio_management.py comparisionTestSeveral -> Diff -> {Diff}\n")
                
                # Writing on a .txt file
                with open('results_compare.txt','a') as txtfile:
                    if Diff:
                        self.csv_names.append(f'{model_name}')
                        self.diff_num += 1
                        txtfile.write(f" - {model_name} : NOT OK - see {model_name}.csv for more details. \n")
                    if Diff == False:
                        txtfile.write(f" - {model_name} : OK \n")
                    txtfile.close()
                
        with open('results_compare.txt','a') as txtfile:
            txtfile.write("\n##### STATS #####\n")
            txtfile.write(f" - {self.diff_num} models over {len(self.modelList)} models have unequal simulation results. \n")
        txtfile.close()
        pass
        
    def csvCompact(self):
        # Initialization
        wdir = path.join(repo_path,'devtest_thermosyspro/Dev_TestSuite/data')
        rowsList= [] # will contain, for each file, the comprehensive list compounds of the row of the file
        
        # Scrap and read .csv files
        for (dirpath, dirnames, filenames) in walk(wdir):
            
            # Prints
            # print(f'\ndirpath : {dirpath}\n')
            # print(f'\ndirnames : {dirnames}\n')
            # print(f'\nfilenames : {filenames}\n')
            path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data\results_compare')
            if not (path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data\results_compare') in dirpath):
                for filename in filenames:
                    
                    # Prints
                    # print(f"\nfilename.endswith('.csv') : {filename.endswith('.csv')}\n")
                    
                    if filename.endswith('_csv.csv'):
                        os.chdir(dirpath)
                        with open(f'{filename}', newline="") as csvfile:
                            reader = csv.DictReader(csvfile, delimiter=';')
                            rowsList.append([row for row in reader])
        #csvfile.close()
        
        # Initialization
        os.chdir(wdir)
        fieldnames = [key for key in rowsList[0][0].keys()]
        
        # Prints
        # print(f"-- PRINT -- \nio_management.py csvCompact -> rowsList -> {rowsList}\n")
        # print(f"-- PRINT -- \nio_management.py csvCompact -> fieldnames -> {fieldnames}\n")
        
        # Write the scrapped rows in a new .csv file 
        with open('logfile_csv.csv', "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for rows in rowsList:
                for row in rows:
                    try:
                        writer.writerow(row)
                    except Exception as err: 
                        print(f'csvCompact -> Exception : {err}')
        #csvfile.close()
                    
        # Create html_csv file as logfile_csv file transposed
        pd.read_csv('logfile_csv.csv', sep = ';', header=None).T.to_csv('html_csv.csv', sep = ';', header=False, index=False)
        
        # Fieldnames recuperation
        with open('html_csv.csv', 'r') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            rows = [row for row in reader]
            fieldnames = list(rows[0].keys())
        infile.close()
        
        # Fieldnames reorder
        print(f"-- PRINT -- \nio_management.py csvCompact -> fieldnames -> {fieldnames}\n")
        if 'check' in fieldnames:
            check_index = fieldnames.index('check')
        
        if 'translate' in fieldnames:
            translate_index = fieldnames.index('translate')

        newfieldnames = []
        newfieldnames = fieldnames[0:check_index + 1]
        newfieldnames += fieldnames[translate_index:]
        newfieldnames += fieldnames[check_index + 1:translate_index]
        print(f"-- PRINT -- \nio_management.py csvCompact -> newfieldnames -> {newfieldnames}\n")
        
        # Columns reorder
        with open('html_reordered_csv.csv', 'w+') as outfile:
            # output dict needs a list for new column ordering
            writer = csv.DictWriter(outfile, fieldnames=newfieldnames, delimiter=';')
            # reorder the header first
            writer.writeheader()
            for row in rows:
                # writes the reordered rows to the new file
                writer.writerow(row)
        outfile.close()
    
    def csvCall(self, call):
        """
        ...
        
        Parameters
        ----------
        ... : ...
            ...

        Returns
        -------
        ...
        """
        # Prints
        # print(f"-- PRINT -- \nio_management.py csvCall -> bool 1 & 2 -> {bool(call == 'translate' and self.paramsDico['translateResultsDico']['warnings'])}\n")
        # print(f"-- PRINT -- \nio_management.py csvCall -> bool 1 -> {bool(call == 'translate')}\n")
        # print(f"-- PRINT -- \nio_management.py csvCall -> bool 2 -> {bool(self.paramsDico['translateResultsDico']['warnings'])}\n")
        
        # Init
        self.call = call
        
        # Directories Settings
        self.wdir = path.join(repo_path,f'devtest_thermosyspro/Dev_TestSuite/data/{call}_results')
        
        # Checking for warnings following by translate_warnings_csv.csv file generation if it is
        if self.paramsDico[f'{call}ResultsDico']['warnings']:
            self.csvWarningGen()
            pass
        
        if self.paramsDico[f'{call}ResultsDico']['timers']:
            self.csvTimersGen()
            
        self.csvResultsGen()
        
        pass
    
    def csvGen(self, fieldnames, dico, name):
        """
        ...
        
        Parameters
        ----------
        ... : ...
            ...

        Returns
        -------
        ...
        """
        try:
            # Directories settings
            os.chdir(self.wdir)
            isfile = os.path.isfile(f'./{name}.csv')
            
            # Csv settings            
            with open(f'{name}.csv', "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                
                if not isfile:
                    print(f'There is no {name}.csv file, {name}.csv file creation...')
                    writer.writeheader()
                
                else:
                    print(f'There is a {name}.csv file, putting in data...')
                
                writer.writerow(dico)
                #csvfile.close()
            
            return True
        
        except OSError as err:
            print(f'error during the {name}.csv file generation : {err}')
            return False

    def csvTimersGen(self):
        """
        
        Returns
        -------
        bool
            DESCRIPTION.
    
        """
        # Csv settings
        self.timersDico = self.paramsDico[f'{self.call}ResultsDico']['timers']
        fieldnames = [key for key in self.timersDico.keys()]
        fieldnames.insert(0, 'Info / Models')
        rowsDico = self.dico4csvTimersGen()
        
        # Prints
        # print(f"-- PRINT -- \nio_management.py csvWarningGen -> self.warningsDico -> {self.warningsDico}\n")
        # print(f"-- PRINT -- \nio_management.py csvWarningGen -> rowsDico -> {rowsDico}\n")
        
        # Loop on the row to insert in the csv file
        for timers, rowDico in rowsDico.items():
            
            rowDico['Info / Models'] = f'{timers}'
            
            # Prints
            # print(f"-- PRINT -- \nio_management.py csvWarningGen -> rowDico -> {rowDico}\n")
        
            csvtimersgen_result = self.csvGen(fieldnames, rowDico, 'timers_csv')
            
        return csvtimersgen_result
    
    def dico4csvTimersGen(self):
        """
        rows generation to complete the warning_csv.csv file
    
        Returns
        -------
        rows : dictionnary
            a dictionnary structured as follow {'warning type' : {'class name': bool value}}
        """
        # Models class name collect
        tmp = [class_name for class_name in self.timersDico.keys()]
        
        # Rows Dico Init
        rowsDico = {timer_name : None for timer_name in self.timersDico[tmp[0]].keys()} if self.call == 'simulation' else {timer_name : None for timer_name in self.timersDico[tmp[0]].keys()}
            
        # Loop on the different warning type
        for timer_name in rowsDico.keys():
            rowDico = {}
            
            # Loop on the different model
            for class_name, timersubDico in self.timersDico.items():
                rowDico[f"{class_name}"] = timersubDico[f"{timer_name}"]
            
            rowsDico[f"{timer_name}"] = rowDico
                
            # Prints
            # print(f"-- PRINT -- \n io_management.py dico4csvWarningGen -> rowDico -> {rowDico}\n")
          
        # Prints                    
        # print(f"-- PRINT -- \n io_management.py dico4csvWarningGen -> rowsDico -> {rowsDico}\n")
        
        return rowsDico              
        
    def csvResultsGen(self):
        """
        ...
        
        Parameters
        ----------
        ... : ...
            ...

        Returns
        -------
        ...
        """ 
        # Init
        self.resultsDico = self.paramsDico[f'{self.call}ResultsDico']['results']
        
        # Csv settings
        fieldnames = [key for key in self.resultsDico.keys()]
        fieldnames.insert(0, 'Info / Models')
        self.resultsDico['Info / Models'] = f'{self.call}'
                    
        csvgen_result = self.csvGen(fieldnames, self.resultsDico, 'results_csv')
        return csvgen_result
        
    def csvWarningGen(self):
        """
        
        Returns
        -------
        bool
            DESCRIPTION.
    
        """
        # Csv settings
        self.warningsDico = self.paramsDico[f'{self.call}ResultsDico']['warnings']
        fieldnames = [key for key in self.warningsDico.keys()]
        fieldnames.insert(0, 'Info / Models')
        rowsDico = self.dico4csvWarningGen()
        
        # Prints
        # print(f"-- PRINT -- \nio_management.py csvWarningGen -> self.warningsDico -> {self.warningsDico}\n")
        # print(f"-- PRINT -- \nio_management.py csvWarningGen -> rowsDico -> {rowsDico}\n")
        
        # Loop on the row to insert in the csv file
        for warning_type, rowDico in rowsDico.items():
            
            rowDico['Info / Models'] = f'{warning_type}'
            
            # Prints
            # print(f"-- PRINT -- \nio_management.py csvWarningGen -> rowDico -> {rowDico}\n")
            
            csvwarninggen_result = self.csvGen(fieldnames, rowDico, 'warning_csv')
            
        return csvwarninggen_result
    
    def dico4csvWarningGen(self):
        """
        rows generation to complete the warning_csv.csv file

        Returns
        -------
        rows : dictionnary
            a dictionnary structured as follow {'warning_name' : {'class name': bool value}}
        """
        # Models class name collect
        tmp = [class_name for class_name in self.warningsDico.keys()]
        
        # Rows Dico Init
        rowsDico = {warning_name : None for warning_name in self.warningsDico[tmp[0]].keys()}
        
        # Prints
        # print(f"-- PRINT -- \n io_management.py dico4csvWarningGen -> self.warningsDico -> {self.warningsDico}\n")
        
        # Loop on the different warning type
        for warning_name in rowsDico.keys():
            rowDico = {}
            
            # Loop on the different model
            for class_name, warningsubDico in self.warningsDico.items():
                # print(f"{warning_name}")
                rowDico[f"{class_name}"] = warningsubDico[f"{warning_name}"]
            
            rowsDico[f"{warning_name}"] = rowDico
                
            # Prints
            # print(f"-- PRINT -- \n io_management.py dico4csvWarningGen -> rowDico -> {rowDico}\n")
           
        # Prints           
        # print(f"-- PRINT -- \n io_management.py dico4csvWarningGen -> rowsDico -> {rowsDico}\n")
        
        return rowsDico
    
    def getModel(self, start_path, keyword):
        """
        Collecting the models, with no dupes, in the subdirectories if their path contains the specific keyword,
        starting from the initial path.
        
        Parameters
        ----------
        start_path : STR
            starting point of the os.walk function
        
        keyword : STR
            keyword to search in directories tree

        Returns
        -------
        None.
        """
        self.start_path = start_path
        self.keyword = keyword
        self.model4simu = {}
        
        for (dirpath, dirnames, filenames) in walk(start_path):
            
            # Prints
            # print(f"-- PRINT -- \nio_management.py getModel -> dirpath -> {dirpath}")
            # print(f"-- PRINT -- \nio_management.py getModel -> dirnames -> {dirnames}")
            # print(f"-- PRINT -- \nio_management.py getModel -> filenames -> {filenames}")
            
            if f'{keyword}' in dirpath:
                for file in filenames:
                    if "package" not in file and  ".mo" in file:
                        if file not in [model for modelsubList in self.model4simu.values() for model in modelsubList]:        
                            if str(dirpath) in self.model4simu.keys():
                                self.model4simu[str(dirpath)].append(str(file))
                            else:
                                self.model4simu[str(dirpath)] = []
                                self.model4simu[str(dirpath)].append(str(file))
                                
        self.modelList = [model for modelsubList in self.model4simu.values() for model in modelsubList]
        pass
    
    # turn the generated csv file into csv files of expected format that are named by
    # the model names where there are variable value differences during the simulation,
    # for instance an edited csv file can be named with "ReqSysPro.Examples.
    # Conditions.CheckInPCount.csv"
    def csvReformat(self, csv_names):
        dic = {}
        data = []
        new_pathlist = []
        try:
            with open(self.paramsDico['csv_path'], 'r', newline="") as csvfile_old:
                reader = csv.reader(csvfile_old, delimiter=';')
                rows = [row for row in reader]
                
                # Prints
                # print(f'-- PRINT -- \ncsvReformat -> rows[0] -> {rows[0]}')
                
                for row in rows:
                    if (row[0], row[1]) not in dic.keys():
                        dic[(row[0], row[1])] = [[row[2], row[3], row[4], row[5]]]
                    else:
                        dic[(row[0], row[1])].append([row[2], row[3], row[4], row[5]])
        
        except FileNotFoundError as err:
            print(f'FileNotFoundError : {err}')
            return 0
        
        new_keys = [(float(time), name) for (time, name) in dic.keys()]
        for csv_name in csv_names:
            new_path = path.join(repo_path,f'devtest_thermosyspro/Dev_TestSuite/data/results_compare/{csv_name}.csv')
            with open(new_path, 'w+', newline="") as csvfile_new:
                f = csv.writer(csvfile_new, delimiter=';')
                for key in sorted(new_keys, key=operator.itemgetter(1, 0)):
                    
                    # print(f'-- PRINT -- \ncsvReformat -> csv_name -> {csv_name}')
                    # print(f'-- PRINT -- \ncsvReformat -> key -> {key}')
                    
                    val = dic[str(key[0]), key[1]]
                    data = [str(key[0]), csv_name]
                    val = sorted(val, key=operator.itemgetter(0))
                    
                    # print(f'-- PRINT -- \ncsvReformat -> val -> {val}')
                    # print(f'-- PRINT -- \ncsvReformat -> data1-> {data}')
                    
                    for j in range(len(val)):
                        if data == []:
                            data = [str(key[0]), csv_name]
                        
                        data.append(val[j][0])
                        data.append(val[j][1])
                        data.append(val[j][2])
                        data.append(val[j][3])
                        
                        # print(f'-- PRINT -- \ncsvReformat -> data2 -> {data}')
                    
                        if key[1] == csv_name:
                            f.writerow(data)
                            del data[:]    
                            
            new_pathlist.append(new_path)
        return new_pathlist
    
    # write the data of mat files into dictionary, where the variable names serve as
    # dictionary keys, the time instants and the variable values serve as dictionary values
    def get_matvaluesDico(self, matfile):
        varDico = {}
        for var in matfile.varNames():
            data = matfile.values(var)
            time = data[0]
            values = data[1]
            varDico[var] = [time, values]
        return varDico
    
    def setParams(self, **kwargs):
        if kwargs:
            for variable, value in kwargs.items():
                self.paramsDico[f'{variable}'] = value

    # Generate the csv file path for each model
    # CALL -> csvReformat
    # CALL -> add_header
    def csvSplit(self):
        new_pathlist = self.csvReformat(self.csv_names)
        #os.remove(csv_pathname)
        
        # Prints
        # print(f'-- PRINT -- \nmain -> new_pathlist -> {self.new_pathlist}')
        
        if new_pathlist:
            for path in self.new_pathlist: # shadowed os.path
               add_header(path)
            return True
        return False

###############################################################################
#                                  MAIN                                       #
###############################################################################

if __name__ == '__main__':
    print('main : io_management')
    
    #from general_modules.generate_help_files import create_help_file
    
    #help_file_path = path.join(getcwd(),pardir,pardir,'Help','modelica_libraries','help_automatic_simulation.txt')
    #list_objects = [Automatic_Simulation]
    
    #create_help_file(help_file_path,list_objects)