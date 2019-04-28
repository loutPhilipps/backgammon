# -------------------------------------------------------------------------------
# Affichage graphique du Backgammon
# -------------------------------------------------------------------------------

import tkinter as tk
import tkinter.messagebox as messagebox
import backgammon as bg
import webbrowser
import pickle
import os


class Lanceur:
    def __init__(self):
        self.score = [0, 0]
        self.base = tk.Tk()
        self.base.configure(background="#534d41")
        self.base.title("Backgammon")
        self.base.wm_iconbitmap("src/images/icone.ico")
        self.base.protocol('WM_DELETE_WINDOW', self.quitter)
        self.base.rowconfigure(0, weight=1)
        self.base.columnconfigure(0, weight=1)
        self.titre = tk.Label(
            self.base, text="Bienvenue dans mon Backgammon", bg="#534d41", fg="white", font=("Helvetica", 16, "bold"))
        self.texte = tk.Label(
            self.base, text="Explication des règles du backgammon", fg="yellow", cursor="hand2", bg="#534d41", font=("Helvetica", 10))
        self.texte.bind("<Button-1>", self.ouvrirRegles)
        self.boutonCharger = tk.Button(
            self.base, text="Charger une partie", command=self.chargerUnePartie)
        self.boutonQuitter = tk.Button(
            self.base, text="Quitter", command=self.quitter)
        self.boutonLancer = tk.Button(
            self.base, text="Lancer une partie", command=self.lancerJeu)
        self.scoreText = tk.StringVar()
        self.scoreText.set("Score du joueur blanc: {}\nScore du joueur noir: {}".format(
            self.score[0], self.score[1]))
        self.scoresLabel = tk.Label(
            self.base, textvariable=self.scoreText, bg="#534d41", fg="white")
        self.titre.grid(column=0, row=0, columnspan=4)
        self.boutonQuitter.grid(column=2, row=3, columnspan=2)
        self.scoresLabel.grid(column=0, row=2, columnspan=2, rowspan=2)
        self.boutonLancer.grid(column=2, row=1, columnspan=2)
        self.boutonCharger.grid(column=2, row=2, columnspan=2)
        self.texte.grid(column=0, row=1, columnspan=2)

    def quitter(self):
        """Quitte"""
        messagebox.showinfo("Bye !", "Au revoir !")
        self.base.destroy()

    def ouvrirRegles(self, evenement):
        webbrowser.open_new(
            r"http://www.jeu-backgammon.net/regles-backgammon.html")

    def demarrer(self):
        self.base.mainloop()

    def lancerJeu(self):
        """Lance des parties tant qu'on ne quitte pas"""
        self.base.withdraw()
        bg.Backgammon(self)

    def lancerSauvegarde(self):
        choix = self.choixSauvegarde.curselection()
        if choix == ():
            messagebox.showwarning(
                "Charger", "Sélectionnez une partie à charger")
        else:
            try:
                self.fenetreChoix.destroy()
                self.chargerJeu(self.listeSauvegardes[choix[0]])
            except:
                messagebox.showerror(
                    "Erreur", "Impossible de charger la partie !")

    def chargerUnePartie(self):
        self.listeSauvegardes = os.listdir("sauvegardes")
        self.fenetreChoix = tk.Toplevel()
        self.fenetreChoix.title("Choisissez une sauvegarde")
        self.boutonQuitter = tk.Button(
            self.fenetreChoix, text="Quitter", command=self.fenetreChoix.destroy)
        self.boutonCharger = tk.Button(
            self.fenetreChoix, text="Charger cette partie", command=self.lancerSauvegarde)
        self.choixSauvegarde = tk.Listbox(
            self.fenetreChoix, selectmode="single")
        self.choixSauvegarde.insert("end", *self.listeSauvegardes)
        self.choixSauvegarde.grid()
        self.boutonCharger.grid()
        self.boutonQuitter.grid()

    def chargerJeu(self, sauvegarde):
        fichier = open("sauvegardes/" + sauvegarde, "rb")
        [jeu, prison, prochainJoueur] = pickle.load(fichier)
        fichier.close()
        self.base.withdraw()
        bg.Backgammon(self, jeu, prison, prochainJoueur)

    def vainqueur(self, champion, valeurPartie):
        """Ajoute le score de la partie au vainqueur"""
        self.score[champion] += valeurPartie
        self.scoreText.set("Score du joueur blanc: {}\nScore du joueur noir: {}".format(
            self.score[0], self.score[1]))

    def montreScores(self):
        return self.score
