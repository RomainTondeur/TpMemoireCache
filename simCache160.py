print("------------------------")
print("SIMULATION MEMOIRE CACHE")
print("------------------------")

# Auteurs: LAMPE Ronan / TONDEUR Romain
# Description: Script Python de Simulation d'une Mémoire Cache
# Execution: python3 simCache160.py cs bs assoc trace_mem
#   avec cs=cache_size / bs=bloc_size / assoc=degre_associativite / trace_mem=fichier_trace_memoire


# Importation des modules
import sys
import os


# Arguments donnés à l'appel du script
print("\nLecture des paramètres...")
args = sys.argv[1:]


# Déclaration des variables
cs = 0
bs = 0
assoc = 0
trace_mem = ""


# Vérification de la récupération des paramètres (& affectation)
if len(args) == 4:

    cs = int(args[0])
    print("Taille de la cache.. " + str(cs) + " octets")

    bs = int(args[1])
    print("Taille d'un bloc.. " + str(bs) + " octets")

    assoc = int(args[2])
    print("Degré d'associativité.. " + str(assoc))

    if os.path.exists(args[3]):
        trace_mem = args[3]
        print("Trace mémoire.. " + trace_mem + " (trouvé)")
    else:
        print("Erreur: Trace mémoire introuvable")
        exit(1)
else:
    print("Erreur: " + str(4 - len(args)) + " Paramètres manquants")
    exit(1)


# Affichage du type de cache
print("\nRecherche du type de cache...")
if assoc == 1:
    print("Cache à accès direct (DMC)")
elif assoc == (cs % bs):
    print("Cache totalement associatif")
else:
    print("Cache de type inconnu")


# Ouverture & Lecture de la trace
print("\nOuverture de la trace mémoire...")
trace = open(trace_mem, "r")
print("Lecture et enregistrement de la trace mémoire..")
instructions = trace.readlines()
print("La trace mémoire a bien été lue")


# Fermeture de la trace
trace.close()
