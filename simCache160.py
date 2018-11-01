
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

# Nb succès en lecture
suc_lec = 0
# Nb succès en écriture
suc_ecr = 0
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

        # Initialisation de la file (historique) FIFO & LRU
        self.file_fifo_lru = [list(range(self.assoc)) for _ in range(self.nbe)]

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
            print("Cache totalement associatif")
        else:
            print("Cache associatif à " + str(self.assoc) + " ensembles")

    # Lecture de la trace (EN CONSTRUCTION)
    def lecture_trace(self):
        print("\nOuverture de la trace mémoire...")
        with open(self.trace_mem, "r") as trace:
            print("Récupération du contenu de la trace mémoire..")
            for inst in trace.readlines():
                global suc_lec
                global suc_ecr
                global def_lec
                global def_ecr
                global code_rempl

                # Type d'instruction
                type_inst = inst[0]

                # Numéro de bloc
                numbloc = int(inst[1:], 16) / self.bs

                # Index
                index = int(numbloc) % self.nbe

                # Etiquette
                tag = int(numbloc / self.nbe)

                for assoc in range(self.assoc):
                    if not self.cache[index][assoc].valide or self.cache[index][assoc].tag != tag:
                        pass
                    else:
                        # Etiquette trouvée dans un bloc de la cache -> Hit
                        if type_inst == 'R':
                            suc_lec += 1
                        elif type_inst == 'W':
                            suc_ecr += 1

                        if code_rempl == 1:
                            self.file_fifo_lru[index].pop(self.file_fifo_lru[index].index(assoc))
                            self.file_fifo_lru[index].append(assoc)

                        break
                else:
                    # Etiquette introuvable dans les blocs de la cache -> Miss
                    if type_inst == 'R':
                        def_lec += 1
                    elif type_inst == 'W':
                        def_ecr += 1

                    # On écrit alors l'étiquette dans la cache selon le code de remplacement
                    if code_rempl == 0 or code_rempl == 1:
                        self.fifo_lru(index, tag)
                    elif code_rempl == 2:
                        self.nru(index, tag)
                    elif code_rempl == 3:
                        self.rand(index, tag)
        print("La trace mémoire a bien été lue")

    # First in, First out (FiFo) & Least Recently Used (LRU)
    def fifo_lru(self, index, tag):
        assoc = self.file_fifo_lru[index][0]
        self.cache[index][assoc].valide = True
        self.cache[index][assoc].tag = tag
        self.file_fifo_lru[index].pop(0)
        self.file_fifo_lru[index].append(assoc)

    # TO-DO: Not Recently Used
    def nru(self, index, tag):
        pass

    # TO-DO: Random
    def rand(self, index, tag):
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
    print("Nombre total de succès en lecture.. " + str(suc_lec) + " (" + str(round((suc_lec / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")
    print("Nombre total de succès en écriture.. " + str(suc_ecr) + " (" + str(round((suc_ecr / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")
    print("Nombre total de succès de cache.. " + str(suc_lec + suc_ecr) + " (" + str(round(((suc_lec + suc_ecr) / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")
    print("...\nNombre total de défauts en lecture.. " + str(def_lec) + " (" + str(round((def_lec / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")
    print("Nombre total de défauts en écriture.. " + str(def_ecr) + " (" + str(round((def_ecr / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")
    print("Nombre total de défauts de cache.. " + str(def_lec + def_ecr) + " (" + str(round(((def_lec + def_ecr) / (suc_lec + suc_ecr + def_lec + def_ecr)) * 100, 2)) + "% du total)")


# ----------------------------------------------------------------------
# -------------------------- MAIN DU SCRIPT ----------------------------
# ----------------------------------------------------------------------

# Calcul du CODE
calcul_code()

print("\n -------------------------- ")
print("| SIMULATION MEMOIRE CACHE |")
print(" -------------------------- ")

# On crée notre instance de mémoire cache
params = ["4096", "64", "4", "mergesort2000Trace.txt"]
MemCache = Memoire(verif_parametrage(params))
MemCache.affiche_params()

# Recherche du type de mémoire cache
MemCache.type_cache()

# Lecture de la trace mémoire (EN CONSTRUCTION)
MemCache.lecture_trace()

# Affichage des indicateurs de Hits/Misses
affiche_indics()
