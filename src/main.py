import affichage

import os
if not os.path.exists("sauvegardes"):
    os.makedirs("sauvegardes")


monEcranDeDemarrage = affichage.Lanceur()
monEcranDeDemarrage.demarrer()
