
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
# ----------------------------- CLASSES --------------------------------
# ----------------------------------------------------------------------

# Classe d'un bloc mémoire
class Bloc(object):
    # Procédure d'initialisation
    def __init__(self):
        #
        self.valide = False

        # Etiquette
        self.tag = int(0)

    # Affichage de la classe
    def __repr__(self):
        return "Bloc({}|{})".format(self.valide, self.tag)


# Classe de la mémoire cache
class Memoire:

    # ----------------------------------------------------------------------
    # --------------------------- PROCEDURES -------------------------------
    # ----------------------------------------------------------------------

    # Procédure d'initialisation
    def __init__(self, params):
        # Cache size (taille totale de la cache, octet)
        self.cs = params[0]

        # Block size (taille d'un bloc, octet)
        self.bs = params[1]

        # Degré d'associativité du cache
        self.assoc = params[2]

        # Chemin du fichier de trace mémoire (nom de la trace si même dossier source)
        self.trace_mem = params[3]

        # Nombre d'ensembles
        self.nbe = int(self.cs / (self.bs * self.assoc))

        # Initialisation de la cache mémoire avec "nbe" lignes
        self.cache = [[] for _ in range(self.nbe)]
        for index in range(len(self.cache)):
            # Pour chaque ligne, on initialise "assoc" "Bloc" et on les lient à la cache
            self.cache[index].extend(Bloc() for _ in range(self.assoc))

    # Affichage des paramètres récupérés
    def affiche_params(self):
        print("Taille de la cache.. " + str(self.cs) + " octets")
        print("Taille d'un bloc.. " + str(self.bs) + " octets")
        print("Degré d'associativité.. " + str(self.assoc))
        print("Nombre d'ensembles.. " + str(self.nbe))
        print("Trace mémoire.. " + os.path.abspath(self.trace_mem))

    # Recherche du type du cache
    def type_cache(self):
        print("\nRecherche du type de cache en cours...")
        if self.assoc == 1:
            print("Cache à accès direct (DMC)")
        elif self.assoc == (self.cs % self.bs):
            print("Cache 100% associatif")
        else:
            print("Cache de type inconnu ou erreur de paramétrage")

    # Lecture de la trace (EN CONSTRUCTION)
    def lecture_trace(self):
        print("\nOuverture de la trace mémoire...")
        with open(self.trace_mem, "r") as trace:
            print("Récupération du contenu de la trace mémoire..")
            for inst in trace.readlines():

                # Numéro de bloc
                numbloc = int(int(inst[1:], 16) / self.bs)

                # Index
                index = numbloc % self.nbe

                # Etiquette
                tag = int(numbloc / self.nbe)

                assoc = 0
                trouve = False
                while assoc < self.assoc and not trouve:
                    if not self.cache[index][assoc].valide or self.cache[index][assoc].tag != tag:
                        assoc += 1
        print("La trace mémoire a bien été lue")

    # TO-DO: Random
    def rand(self):
        pass

    # TO-DO: First in, First out (FiFo)
    def fifo(self):
        pass

    # TO-DO: Least Recently Used (LRU)
    def lro(self):
        pass


# Vérification de la récupération des paramètres (& affectation)
def verif_parametrage():
    # Récupération des arguments passés au script
    print("\nLecture des paramètres...")
    arguments = sys.argv[1:]
    param_ok = True

    # On vérifie si on récupère bien 4 arguments
    if len(arguments) == 4:
        cs = arguments[0]
        bs = arguments[1]
        assoc = arguments[2]
        trace_mem = arguments[3]

        # On vérifie si le cache size est du bon type
        if not str.isdigit(cs):
            print("Erreur: Le type du paramètre \"cs\" est invalide")
            param_ok = False

        # On vérifie si le block size est du bon type
        if not str.isdigit(bs):
            print("Erreur: Le type du paramètre \"bs\" est invalide")
            param_ok = False

        # On vérifie si le degré d'associativité est du bon type
        if not str.isdigit(assoc):
            print("Erreur: Le type du paramètre \"assoc\" est invalide")
            param_ok = False

        # On vérifie si le fichier de trace mémoire existe
        if not os.path.exists(trace_mem):
            print("Erreur: Fichier de trace mémoire introuvable")
            param_ok = False

        # Si les paramètres sont valides -> on retourne la liste des arguments castés
        # Sinon -> On arrête le script
        if param_ok:
            return [int(cs), int(bs), int(assoc), trace_mem]
        else:
            exit(1)
    else:
        print("Erreur: " + str(4 - len(arguments)) + " paramètres manquants")
        exit(1)


# ----------------------------------------------------------------------
# -------------------------- MAIN DU SCRIPT ----------------------------
# ----------------------------------------------------------------------

print(" -------------------------- ")
print("| SIMULATION MEMOIRE CACHE |")
print(" -------------------------- ")

# On crée notre instance de mémoire cache
MemCache = Memoire(verif_parametrage())
MemCache.affiche_params()

# Recherche du type de mémoire cache
MemCache.type_cache()

# Lecture de la trace mémoire (EN CONSTRUCTION)
# MemCache.lecture_trace()
