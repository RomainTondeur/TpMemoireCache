
# Auteurs: LAMPE Ronan / TONDEUR Romain
# Description: Script Python de Simulation d'une Mémoire Cache
# Execution: python3 simCache160.py cs bs assoc trace_mem
#   avec cs=cache_size / bs=bloc_size / assoc=degre_associativite / trace_mem=fichier_trace_memoire


# Importation des modules
import sys
import os


# Arguments donnés à l'appel du script
args = sys.argv[1:]


# Déclaration des variables
cs = 0
bs = 0
assoc = 0
trace_mem = ""


# Vérification de la récupération des paramètres (& affectation)
if len(args) == 4:
    cs = args[0]
    bs = args[1]
    assoc = args[2]
    if os.path.exists(args[3]):
        trace_mem = args[3]
    else:
        print("Erreur: Trace mémoire introuvable")
        exit(1)
else:
    print("Erreur: " + str(4 - len(args)) + " Paramètres manquants")
    exit(1)


# Affichage des paramètres
print("\n--------------- PARAMETRES ---------------")
print("Taille de la cache: " + str(cs) + " octets")
print("Taille d'un bloc: " + str(bs) + " octets")
print("Degré d'associativité: " + str(assoc))
print("Trace mémoire: " + trace_mem)


# Ouverture & Lecture de la trace
trace = open(trace_mem, "r")
instructions = trace.readlines()

print("\n--------------- LECTURE TRACE ---------------")
print("Info: La trace mémoire a bien été lue")


# Fermeture de la trace
trace.close()
