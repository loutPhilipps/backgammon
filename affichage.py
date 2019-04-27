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
        self.boutonLancer.pack()
        self.base.mainloop()

    def lancerJeu(self):
        self.base.destroy()
        self.jeu = BackgammonGraphique()


class BackgammonGraphique:
    def __init__(self):
        self.jeu = bg.Backgammon()
        self.base = tk.Tk()
        self.base.title("Mon Backgammon (par Adam Philipps)")
        self.canvas = tk.Canvas(self.base)
        self.canvas.pack()
        self.photo = tk.PhotoImage(file="./plateau.png")
        self.canvas.create_image(100, 80, image=self.photo)
        self.boutonQuitter = tk.Button(
            self.base, text="Quitter", command=self.base.destroy)
        self.boutonQuitter.pack()
        self.base.mainloop()
