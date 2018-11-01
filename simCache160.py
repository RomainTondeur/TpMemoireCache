
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
import random


# ----------------------------------------------------------------------
# ----------------------- VARIABLES INDICATEURS ------------------------
# ----------------------------------------------------------------------

# Code d'écriture
code_ecrit = 0
# Code de remplacement
code_rempl = 0
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
        # Bit de validation
        self.valide = False

        # Bit de modification
        self.modifie = False

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
    def __init__(self, lst_params_cast):
        # Cache size (taille totale de la cache, octet)
        self.cs = lst_params_cast[0]

        # Block size (taille d'un bloc, octet)
        self.bs = lst_params_cast[1]

        # Degré d'associativité du cache
        self.assoc = lst_params_cast[2]

        # Chemin du fichier de trace mémoire (nom de la trace si même dossier source)
        self.trace_mem = lst_params_cast[3]

        # Nombre d'ensembles
        self.nbe = int(self.cs / (self.bs * self.assoc))

        # Initialisation de la cache mémoire avec "nbe" lignes
        self.cache = [[] for _ in range(self.nbe)]
        for index in range(len(self.cache)):
            # Pour chaque ligne, on initialise "assoc" "Bloc" et on les lie à la cache
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
        global code_rempl

        print("\nOuverture de la trace mémoire...")
        with open(self.trace_mem, "r") as trace:
            print("Récupération du contenu de la trace mémoire..")
            for inst in trace.readlines():
                global tot_lec
                global tot_ecr
                global def_lec
                global def_ecr

                # Type d'instruction
                type_inst = inst[0]

                # Numéro de bloc
                numbloc = int(int(inst[1:], 16) / self.bs)

                # Index
                index = numbloc % self.nbe

                # Etiquette
                tag = int(numbloc / self.nbe)

                for assoc in range(self.assoc):
                    if not self.cache[index][assoc].valide or self.cache[index][assoc].tag != tag:
                        pass
                    else:
                        # Etiquette trouvée dans un bloc de la cache -> Hit
                        if type_inst == 'R':
                            tot_lec += 1
                        elif type_inst == 'W':
                            tot_ecr += 1
                        break
                else:
                    # Etiquette introuvable dans les blocs de la cache -> Miss
                    if type_inst == 'R':
                        def_lec += 1
                    elif type_inst == 'W':
                        def_ecr += 1

                    # On écrit alors l'étiquette dans la cache selon le code de remplacement
                    if code_rempl == 0:
                        self.fifo(tag)
                    elif code_rempl == 1:
                        self.lru(tag)
                    elif code_rempl == 2:
                        self.nru(tag)
                    elif code_rempl == 3:
                        self.rand(tag)
        print("La trace mémoire a bien été lue")

    # TO-DO: First in, First out (FiFo)
    def fifo(self, tag):
        pass

    # TO-DO: Least Recently Used (LRU)
    def lru(self, tag):
        pass

    # TO-DO: Not Recently Used
    def nru(self, tag):
        pass

    # TO-DO: Random
    def rand(self, tag):
        # Génération d'un nombre entier aléatoire entre 1 et cs
        i = int(random.randint(2, self.cs+1)) - 1
        pass


# Dictionnaire des types d'écriture
tp_ecrit = {
    0: "WT (Write Through)",
    1: "WB (Write Back)"
}

# Dictionnaire des types de remplacement
tp_rempl = {
    0: "FIFO (First in, First out)",
    1: "LRU (Least Recently Used)",
    2: "NRU (Not Recently Used)",
    3: "Random"
}


# Calcul du CODE pour le choix du type d'écriture et du type de remplacement des blocs
def calcul_code():
    global code_ecrit
    global code_rempl

    print("\nAuteurs: LAMPE Ronan & TONDEUR Romain")
    code_aut = [ord('L'), ord('T')]
    code_auts = sum(code_aut)
    print("Code: \'L\' + \'T\' = " + str(code_aut[0]) + " + " + str(code_aut[1]) + " = " + str(code_auts))
    code_ecrit = code_auts % 2
    print("Gestion écriture = " + str(code_auts) + " % 2 = " + str(code_ecrit) + " : " + tp_ecrit[code_ecrit])
    code_rempl = code_auts % 4
    print("Remplacement des blocs = " + str(code_auts) + " % 4 = " + str(code_rempl) + " : " + tp_rempl[code_rempl])


# Vérification de la récupération des paramètres (& affectation)
def verif_parametrage(arguments):
    # Récupération des arguments passés au script
    print("\nLecture des paramètres...")
    if not arguments:
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


# Procédure d'affichage des indicateurs
def affiche_indics():
    print("\nRécupération des indicateurs...")
    print("Nombre total de lectures.. " + str(tot_lec))
    print("Nombre total d'écritures.. " + str(tot_ecr))
    print("Nombre total de défauts en lecture.. " + str(def_lec))
    print("Nombre total de défauts en écriture.. " + str(def_ecr))


# ----------------------------------------------------------------------
# -------------------------- MAIN DU SCRIPT ----------------------------
# ----------------------------------------------------------------------

# Calcul du CODE
calcul_code()

print("\n -------------------------- ")
print("| SIMULATION MEMOIRE CACHE |")
print(" -------------------------- ")

# On crée notre instance de mémoire cache
params = ["1024", "32", "4", "multTrace.txt"]
MemCache = Memoire(verif_parametrage(params))
MemCache.affiche_params()

# Recherche du type de mémoire cache
MemCache.type_cache()

# Lecture de la trace mémoire (EN CONSTRUCTION)
MemCache.lecture_trace()

# Affichage des indicateurs de Hits/Misses
affiche_indics()
