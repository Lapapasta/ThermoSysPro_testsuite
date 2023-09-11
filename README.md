# DevTest_ThermoSysPro

Mode opératoire des Tests (en local)

Dans « GIT tests » : dossier « Dev_TestSuite »
Dans dossier « __script__ » ouvrir (dans Spyder, faire glisser) :

•	« config.py » : y mettre chemins d’accès 
-	Le premier : chemin du dossier git sur pc avec le dossier tests
repo_path = r'C:/Users/D88955/Documents/TESTS TSP_NEW/GIT tests'
-	Le dernier : jusqu’au package.mo de TSP à tester (là où on l’a mis sur le pc)
tsp_path = 'C:/Users/D88955/Documents/TESTS TSP_NEW/ThermoSysPro/package.mo'

•	Ouvrir et Lancer « successive_running_script.py » (qui lance « check.py », « translate.py » et « simulation.py » chacun leur tour) + « referencefile_generation.py » (page récapitulative finale)

Tout ce qui est généré va dans un dossier « data » qui est créé automatiquement  dans `Dev_TestSuite`. Par exemple : Page récapitulative (à ouvrir avec explorer est dans « data ») : « logfile_html.html »

Choisir ce qui va être testé : 
Pour tester tous les .mo avec le mot « examples » dans son chemin d’accès : IO_Manager.getModel(path.join(repo_path,r'devtest_thermosyspro\ThermoSysPro'), 'Examples'). 
Cela dans les 4 fichiers : « referencefile_generation.py », « translate.py », « check.py » et « simulation.py » (ce serait mieux de le faire une seule fois dans "config.py")

## Dépendances
- buildingspy
- pandas


## Remarques
-	Quand on vide le dossier « data » pour refaire des tests : peut-être besoin de fermer processus (ctrl+alt+suppr) Dymola 2021x et Python  (à priori avec dernière version des tests il est prévu de faire un « clean » dans le script)
-	De toutes façons vérifier à la fin des tests qu’il n’y a pas de Dymola en processus qui tourne derrière dans le pc (jeton) et si oui forcer l’arrêt

A vérifier :
-	Création automatique du dossier « data » + son « clean » + fermeture de Dymola à la fin des tests
-	Génération de la page récapitulative « logfile_html.html » sans rencontrer de problème

LIENS GITHUB ET GITLAB :
github.com/Lapapasta/ThermoSysPro_testsuite.git
https://gitlab.com/internship4940732/ThermoSysPro_testsuite.git
https://gitlab.pleiade.edf.fr/Phy13Models/modelicalibraries/devtest_thermosyspro
