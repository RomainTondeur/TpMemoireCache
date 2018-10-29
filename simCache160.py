
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


# ----------------------------------------------------------------------
# ----------------------------- CLASSES --------------------------------
# ----------------------------------------------------------------------

# Classe de la mémoire cache
class Memoire:
    # ----------------------------------------------------------------------
    # ------------------------- VARIABLES MEMOIRE --------------------------
    # ----------------------------------------------------------------------

    # Cache size (taille totale de la cache, octet)
    cs = 4096

    # Block size (taille d'un bloc, octet)
    bs = 64

    # Degré d'associativité du cache
    assoc = 4

    # Chemin du fichier de trace mémoire (nom de la trace si même dossier source)
    trace_mem = ""

    # Nombre d'ensembles
    nbe = int(cs / (bs * assoc))

    #
    # numbloc = adr / bs

    # Index
    # index = numbloc % nbe

    # Etiquette
    # tag = numbloc / nbe

    # ----------------------------------------------------------------------
    # --------------------------- PROCEDURES -------------------------------
    # ----------------------------------------------------------------------

    # Vérification de la récupération des paramètres (& affectation)
    def verif_parametrage(self, arguments):
        if len(arguments) == 4:
            self.cs = int(arguments[0])
            print("Taille de la cache.. " + str(self.cs) + " octets")

            self.bs = int(arguments[1])
            print("Taille d'un bloc.. " + str(self.bs) + " octets")

            self.assoc = int(arguments[2])
            print("Degré d'associativité.. " + str(self.assoc))

            if os.path.exists(arguments[3]):
                self.trace_mem = arguments[3]
                print("Trace mémoire.. " + self.trace_mem + " (trouvé)")
            else:
                print("Erreur: Trace mémoire introuvable")
                exit(1)

            self.nbe = int(self.cs / (self.bs * self.assoc))
        else:
            print("Erreur: " + str(4 - len(arguments)) + " Paramètres manquants")
            exit(1)

    # Recherche du type du cache
    def type_cache(self):
        print("\nRecherche du type de cache en cours...")
        if self.assoc == 1:
            print("Cache à accès direct (DMC)")
        elif self.assoc == (self.cs % self.bs):
            print("Cache 100% associatif")
        else:
            print("Cache de type inconnu ou erreur de paramétrage")

    # Lecture de la trace
    def lecture_trace(self):
        print("\nOuverture de la trace mémoire...")
        with open(self.trace_mem, "r") as trace:
            print("Récupération du contenu de la trace mémoire..")
            for inst in trace.readlines():
                pass
        print("La trace mémoire a bien été lue")

    # Random
    def rand(self):
        pass

    # First in, First out (FiFo)
    def fifo(self):
        pass

    # Least Recently Used (LRU)
    def lro(self):
        pass


# ----------------------------------------------------------------------
# ----------------------- VARIABLES INDICATEURS ------------------------
# ----------------------------------------------------------------------

# Nb tot de lectures
tot_lec = 0
# Nb tot d'écritures
tot_ecr = 0
# Nb défauts en lecture
def_lec = 0
# Nb défauts en écriture
def_ecr = 0

# ----------------------------------------------------------------------
# -------------------------- MAIN DU SCRIPT ----------------------------
# ----------------------------------------------------------------------

print(" -------------------------- ")
print("| SIMULATION MEMOIRE CACHE |")
print(" -------------------------- ")

# Récupération des arguments passés au script
print("\nLecture des paramètres...")
arguments = sys.argv[1:]

# On crée notre instance de mémoire cache
MemCache = Memoire()

# Vérification du paramétrage
MemCache.verif_parametrage(arguments)

# Recherche du type de mémoire cache
MemCache.type_cache()

# Lecture de la trace mémoire
MemCache.lecture_trace()
