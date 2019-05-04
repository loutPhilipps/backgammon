
import os
import affichage

# Installation des dépendances
from installation import installe

installe()


if not os.path.exists("sauvegardes"):
    os.mkdir("sauvegardes")

monEcranDeDemarrage = affichage.Lanceur()
