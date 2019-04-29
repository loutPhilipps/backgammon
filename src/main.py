import affichage

import os
if not os.path.exists("sauvegardes"):
    os.mkdir("sauvegardes")

monEcranDeDemarrage = affichage.Lanceur()
