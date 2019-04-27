# -------------------------------------------------------------------------------
# Affichage graphique du Backgammon
# -------------------------------------------------------------------------------

import tkinter as tk
import backgammon as bg


class Lanceur:
    def __init__(self):
        self.base = tk.Tk()
        self.base.title("Backgammon")
        self.boutonLancer = tk.Button(
            self.base, text="Lancer le jeu !", command=self.lancerJeu)
        self.checkBoxPari = tk.Checkbutton(self.base)
        self.checkBoxPari.pack()
        self.boutonLancer.pack()
        self.score = [0, 0]
        self.base.mainloop()

    def lancerJeu(self):
        """Lance des parties tant qu'on ne quitte pas"""
        self.base.destroy()
        bg.Backgammon(self)

    def vainqueur(self, champion, valeurPartie):
        """Ajoute le score de la partie au vainqueur"""
        self.score[champion] += valeurPartie

    def montreScores(self):
        return self.score
