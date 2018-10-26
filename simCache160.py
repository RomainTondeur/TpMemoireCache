
# Auteurs: LAMPE Ronan / TONDEUR Romain
# Description: Script Python de Simulation d'une Mémoire Cache
# Execution: python3 simCache160.py cs bs assoc trace_mem
#   avec cs=cache_size
#   /    bs=bloc_size
#   /    assoc=degre_associativite
#   /    trace_mem=fichier_trace_memoire


# Importation des modules
import sys
import os


print("------------------------")
print("SIMULATION MEMOIRE CACHE")
print("------------------------")


# Déclaration - Variables paramétrables
cs = 4096
bs = 64
assoc = 4
trace_mem = ""
nbe = cs / (bs*assoc)
# nb = adr / bs
# Index = nb % nbe
# Etiquette = nb / nbe

# Déclaration - Variables indicateurs
tot_lec = 0
tot_ecr = 0
def_lec = 0
def_ecr = 0

# Déclaration - Liste des instructions [["Opérateur"], ["Hexadécimal"]]
instructions = []


# Vérification de la récupération des paramètres (& affectation)
def verif_parametrage():
    global cs
    global bs
    global assoc
    global trace_mem
    global nbe

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

        nbe = cs / (bs*assoc)
    else:
        print("Erreur: " + str(4 - len(args)) + " Paramètres manquants")
        exit(1)


# Recherche du type du cache
def type_cache():
    print("\nRecherche du type de cache en cours...")
    if assoc == 1:
        print("Cache à accès direct (DMC)")
    elif assoc == (cs % bs):
        print("Cache 100% associatif")
    else:
        print("Cache de type inconnu ou erreur de paramétrage")


# Lecture de la trace
def lecture_trace():
    global instructions

    print("\nOuverture de la trace mémoire...")
    with open(trace_mem, "r") as trace:
        print("Récupération du contenu de la trace mémoire..")
        for inst in trace.readlines():
            instructions.append([inst[0], inst[1:]])
    print("La trace mémoire a bien été lue")


# def traitement_inst(): TO-DO


# MAIN DU SCRIPT

# Récupération des arguments passés au script
print("\nLecture des paramètres...")
args = sys.argv[1:]

# Execution des procédures
verif_parametrage()
type_cache()
lecture_trace()


