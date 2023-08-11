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

import csv
import os

###############################################################################
#                                FUNCTION                                     #
###############################################################################

# def rearrangeDico(csv_file):
#     with open(csv_file, 'r') as file:
#         dictreader = csv.DictReader(file, delimiter=';')
#         for row in dictreader:
#             print(row)
#         # each row is a list
#         # data = list(reader)

def csv_to_html(csv_file, html_file, legendsDico):
    with open(csv_file, 'r') as file:
        
        reader = csv.reader(file, delimiter=';')
            
        # each row is a list
        data = list(reader)
        
        # Prints
        # print(f"-- PRINT -- \nhtml_generation main -> list(reader) -> {data} \n")
        
        # warnings index list generation
        warningsnamesList = [elem for elem in data[0] if 'timeout' in elem]
        warningsnamesList += ['tra. w1', 'tra. w2', 'tra. w3', 'tra. others', 'sim. w1', 'sim. w2', 'sim. w3', 'sim. others']
        warningsindexList = [data[0].index(elem) for elem in warningsnamesList if elem in data[0]]

    with open(html_file, 'w') as file:
        file.write('<html>\n')
        file.write('<head>\n')
        file.write("<title>Test suite information's page</title>\n")
        file.write('<style>\n')
        file.write('table, th, td {\n')
        file.write('  border: 1px solid black;\n')
        file.write('  border-collapse: collapse;\n')
        file.write('  padding: 5px;\n')
        file.write('}\n')
        file.write('.green-cell { background-color: #5FF35F; }\n')
        file.write('.grey-cell { background-color: #C6C6C6; }\n')
        file.write('.red-cell { background-color: #F35F5F; }\n')
        file.write('.yellow-cell { background-color: #F3DF5F; }\n')
        file.write('</style>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        
        # Legend
        file.write('<p>\n')
        for key, value in legendsDico.items():
            ligne_html = f"{key} : {value}<br>\n"
            file.write(ligne_html)
        file.write('<p/>\n')
        
        file.write('<table>\n')

        for row in data:
            file.write('<tr>\n')
            iter = 0
            for cell in row:
                if cell == 'True' or cell == 'False':
                    if iter in warningsindexList:
                        cell_class = 'grey-cell' if cell == 'False' else 'yellow-cell'
                        file.write('<td class="{}"></td>\n'.format(cell_class))
                    # Vérifier si la cellule contient 'True' ou 'False' et ajouter la classe CSS appropriée
                    else:
                        cell_class = 'green-cell' if cell == 'True' else 'red-cell'
                        file.write('<td class="{}"></td>\n'.format(cell_class))
                else:
                    file.write('<td>{}</td>\n'.format(cell))
                    
                iter += 1
            file.write('</tr>\n')
            
            
        file.write('</table>\n')
        
        # Parcourir le dictionnaire et écrire les paires clé-valeur dans le fichier HTML
        file.write('</body>\n')
        file.write('</html>\n')

    print("Fichier HTML généré avec succès!")

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
    # Initialization
    os.chdir(path.join(repo_path,r'devtest_thermosyspro\Dev_TestSuite\data'))
    
    # Legend
    frequentwarningList = ['Conflicting start values', 'The following parameters with fixed = false also have a binding', \
                        'Some variables are iteration variables of the initialization problem: but they are not given any explicit start values. Zero will be used.']
    warningnames = ['w1', 'w2', 'w3']
    legendsDico = {warningnames[i] : frequentwarningList[i] for i in range(len(warningnames))}
    
    # Html file generation
    csv_to_html('html_reordered_csv.csv', 'logfile_html.html', legendsDico)
    
    # Remove old .csv file
    # try:
    #     os.remove('logfile_csv.csv')
    #     os.remove('html_csv.csv')
        
    # except OSError as err:
    #     print(f'html_generation -> OSError : {err}')
    #     return -1
    
    return 0

if __name__ == '__main__':
    print('\n--- HTML GENERATION ---\n')
    main()