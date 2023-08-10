# -*- coding: utf-8 -*-
###############################################################################
#                            LIBRARIES IMPORT                                 #
###############################################################################

import re

###############################################################################
#                                 FUNCTIONS                                   #
###############################################################################

def trouver_nombres(chaine):
    # Utilisation d'une expression régulière pour trouver tous les nombres dans la chaîne
    pattern = r'\d+'
    nombres_trouves = re.findall(pattern, chaine)
    return [int(nombre) for nombre in nombres_trouves]

def trouver_premier_nombres(chaine):
    # Utilisation d'une expression régulière pour trouver tous les nombres dans la chaîne
    pattern = r'\d+'
    nombres_trouves = re.find(pattern, chaine)
    return [nombres_trouves]

def get_time(chaine):
    prespaceindex = chaine.find(' ', chaine.find(':'), chaine.find('s'))
    postspaceindex = chaine.find(' ', prespaceindex + 1)
    time = chaine[prespaceindex + 1:postspaceindex]
    return time
  
def last_occurrence_index(main_string, sub_string):
    last_index = main_string.rfind(sub_string)
    return last_index

###############################################################################
#                                    MAIN                                     #
###############################################################################

def main():
    print('main')
        
if __name__ == '__main__':
    print('main')
    main()

