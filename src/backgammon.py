# -------------------------------------------------------------------------------
# Projet Backgammon

# Conventions :
# - noirs: 1, sort en 23
# - blancs: 0, sort en 0
# -------------------------------------------------------------------------------

import random
import tkinter as tk
import tkinter.messagebox as messagebox
import PIL.Image
import PIL.ImageTk
import os
import pickle


def plateauInitial():
    """Place les pions au départ"""
    jeu = [[] for i in range(24)]
    jeu[0] = [1, 1]
    jeu[5] = [0, 0, 0, 0, 0]
    jeu[7] = [0, 0, 0]
    jeu[11] = [1, 1, 1, 1, 1]
    jeu[12] = [0, 0, 0, 0, 0]
    jeu[16] = [1, 1, 1]
    jeu[18] = [1, 1, 1, 1, 1]
    jeu[23] = [0, 0]
    return jeu


class Backgammon:
    def __init__(self, tableauScore, jeu=plateauInitial(), prison=[], prochainJoueur=-1, valeurPartie=1):
        """Création d'un jeu de backgammon"""
        self.jeu = jeu
        self.prison = prison
        if prochainJoueur == -1:
            self.prochainJoueur = random.randint(0, 1)
        else:
            self.prochainJoueur = prochainJoueur

        self.casesPixels = [[] for i in range(24)]
        for i in range(6):
            self.casesPixels[i] = [500-40*(i+1)+1, 500 - 40*i, 0, 200]
        for i in range(6, 12):
            self.casesPixels[i] = [240-40*(i-5) + 1, 240-40*(i-6), 0, 200]
        for i in range(12, 18):
            self.casesPixels[i] = [40*(i-12), 40*(i-11) - 1, 280, 480]
        for i in range(18, 24):
            self.casesPixels[i] = [
                265 + 40*(i-18), 265 + 265*(i-17) - 1, 280, 480]
        # case = [xmin, xmax, ymin, ymax]

        self.tourTermine = False
        self.desJoues = [True, True]
        self.deChoisi = -1
        self.applicationQuittee = False

        # Scores
        self.valeurPartie = valeurPartie
        self.tableauScore = tableauScore

        # Objets Tkinter
        self.base = tk.Tk()
        self.base.title("Mon Backgammon (par Adam Philipps)")
        self.base.wm_iconbitmap("src/images/icone.ico")
        self.imagesDes = [PIL.ImageTk.PhotoImage(
            master=self.base, file="src/images/des/{}.png".format(i)) for i in range(1, 7)]
        self.imagesDesGris = [PIL.ImageTk.PhotoImage(
            master=self.base, file="src/images/des/{}_grey.png".format(i)) for i in range(1, 7)]
        self.imagesPions = [[PIL.ImageTk.PhotoImage(
            master=self.base, file="src/images/pions/{}_{}.png".format(nb, i)) for nb in range(1, 6)] for i in range(2)]
        self.imagesPionsPrison = [[PIL.ImageTk.PhotoImage(master=self.base, image=PIL.Image.open(
            "src/images/pions/{}_{}.png".format(nb, i)).rotate(90, expand=True)) for nb in range(1, 6)] for i in range(2)]
        self.canvasDes = [
            tk.Canvas(self.base, height=200, width=200) for i in range(2)]
        self.canvas = tk.Canvas(self.base, height=500, width=500)
        self.imagePlateau = PIL.ImageTk.PhotoImage(
            master=self.base, file="src/images/plateau.png")
        self.des = (1, 1)
        self.boutonReinitialiser = tk.Button(
            self.base, text="Réinitialiser", command=self.reinit)
        self.boutonSauvegarder = tk.Button(
            self.base, text="Sauvegarder", command=self.sauvegarder)
        self.boutonQuitter = tk.Button(
            self.base, text="Quitter", command=self.quitter)
        scores = self.tableauScore.montreScores()
        textScores = "Score du joueur blanc : {}\nScore du joueur noir : {}".format(
            scores[0], scores[1])
        self.labelScores = tk.Label(
            self.base, text=str(textScores))
        self.prisonCanvas = tk.Canvas(self.base, height=100, width=500)

        self.base.protocol('WM_DELETE_WINDOW', self.quitter)

        # Liaison des images (dés, cases) aux événements
        self.canvasDes[0].bind(
            "<Button-1>", lambda event: self.choisitDe(event, 0))
        self.canvasDes[1].bind(
            "<Button-1>", lambda event: self.choisitDe(event, 1))
        self.canvas.bind(
            "<Button-1>", self.choisitCase)
        self.prisonCanvas.bind(
            "<Button-1>", lambda event: self.choisitCase(event, True))

        self.base.rowconfigure(0, weight=1)
        self.base.columnconfigure(0, weight=1)

        # Ajout des éléments à la fenêtre
        self.canvas.grid(column=0, row=0, rowspan=4)
        self.canvasDes[0].grid(row=0, column=1)
        self.canvasDes[1].grid(row=1, column=1)
        self.prisonCanvas.grid(row=4, column=0, rowspan=3)
        self.boutonSauvegarder.grid(row=4, column=1)
        self.boutonReinitialiser.grid(row=5, column=1)
        self.boutonQuitter.grid(row=6, column=1)
        self.labelScores.grid(row=2, column=1, rowspan=2)

        self.rafraichirAffichage()
        # Lancement du jeu
        self.jouer()

        # Lancement de la fenêtre
        # self.base.mainloop()

    def quitter(self):
        """Quitte la partie et revient au lanceur"""
        self.applicationQuittee = True
        self.base.destroy()
        self.tableauScore.base.deiconify()

    def reinit(self):
        """Réinitialiser"""
        self.base.destroy()
        self.tableauScore.lancerJeu()

    def sauvegarder(self):
        """Sauvegarde la partie"""
        try:
            nb = str(len(os.listdir("sauvegardes")))
            sauvegarde = "sauvegardes/Sauv" + nb
            fichier = open(sauvegarde, "wb")
            pickle.dump([self.jeu, self.prison, self.prochainJoueur], fichier)
            fichier.close()
        except:
            messagebox.showerror(
                "Erreur", "Impossible de sauvegarder la partie !")

    def peutSortir(self, joueur):
        """Vérifie si le joueur peut commencer à sortir ses pions du plateau"""
        if joueur == 0:
            for i in range(6, 24):
                if 0 in self.jeu[i]:
                    return False
            return True
        else:
            for i in range(18):
                if 1 in self.jeu[i]:
                    return False
            return True

    def deEstJouable(self, joueur, valeurDe):
        """Vérifie si le dé peut être joué"""
        for i in range(len(self.jeu)):
            if joueur in self.jeu[i]:
                if self.verifierDeplacement(joueur, valeurDe, i):
                    return True
        return False

    def verifierDeplacement(self, joueur, valeurDe, case):
        """Vérifie si le déplacement est autorisé"""
        if case == -1:
            # prison
            return joueur in self.prison
        else:
            if joueur not in self.jeu[case]:
                # impossible de jouer un pion qui n'existe pas
                return False
            if joueur == 0:
                caseArrivee = case - valeurDe
                autreJoueur = 1
            else:
                caseArrivee = case + valeurDe
                autreJoueur = 0
            if not self.peutSortir(joueur):
                if caseArrivee < 0 or caseArrivee > 23:
                    # essaye de sortir alors que pas encore possible
                    return False
            if autreJoueur in self.jeu[caseArrivee]:
                if len(self.jeu[caseArrivee]) >= 2:
                    # A tout moment, on s'arrange pour que les cases n'aient des pions que d'une seule couleur
                    return False
            elif joueur in self.jeu[caseArrivee]:
                if len(self.jeu[caseArrivee]) >= 5:
                    # 5 pions max d'une couleur
                    return False
        return True

    def lancerDes(self):
        """Lance les dés"""
        return (random.randint(1, 6), random.randint(1, 6))

    def deplacement(self, joueur, valeurDe, case):
        """Déplacement des pions noir et blancs"""
        if joueur == 0:
            if case == -1:
                # prison
                caseArrive = 24 - valeurDe
            else:
                caseArrive = case - valeurDe
            autreJoueur = 1
        else:
            if case == -1:
                # prison
                caseArrive = valeurDe - 1
            else:
                caseArrive = case + valeurDe
            autreJoueur = 0
        if caseArrive < 0 or caseArrive > 23:
            self.jeu[case].remove(joueur)
        if autreJoueur in self.jeu[caseArrive]:
            self.jeu[caseArrive].remove(autreJoueur)
            self.prison.append(autreJoueur)
        if case != -1:
            self.jeu[case].remove(joueur)
        else:
            self.prison.remove(joueur)
        self.jeu[caseArrive].append(joueur)
        self.rafraichirAffichage()

    def aGagne(self, joueur):
        """Vérifie si le joueur a gagné"""
        for case in self.jeu:
            if joueur in case:
                return False
        return True

    def termine(self):
        """Vérifie si le jeu est terminé"""
        for joueur in range(2):
            if self.aGagne(joueur):
                return True
        return False

    def choisitCase(self, event, prison=False):
        if self.desJoues.count(True) > 0:
            self.deChoisi = self.desJoues.index(False)
        if not prison:
            numCase = -1
            for i in range(len(self.casesPixels)):
                if event.x >= self.casesPixels[i][0] and event.x <= self.casesPixels[i][1] and event.y >= self.casesPixels[i][2] and event.y <= self.casesPixels[i][3]:
                    numCase = i
            if numCase != -1:
                # On a bien cliqué sur une case !
                if self.deChoisi != -1:
                    # Un dé a été sélectionné
                    if not self.prochainJoueur in self.jeu[numCase]:
                        # On ne fait rien si le joueur clique sur une case qui ne lui appartient pas
                        pass
                    elif not self.verifierDeplacement(self.prochainJoueur, self.des[self.deChoisi], numCase):
                        messagebox.showinfo(
                            "Déplacement impossible", "Vous n'avez pas le droit de faire ce déplacement")
                    else:
                        self.desJoues[self.deChoisi] = True
                        self.deplacement(self.prochainJoueur,
                                         self.des[self.deChoisi], numCase)
                        self.deChoisi = -1
        else:
            if self.prochainJoueur in self.prison:
                self.deChoisi = -1
                self.desJoues[self.deChoisi] = True
                self.deplacement(self.prochainJoueur,
                                 self.des[self.deChoisi], -1)

    def choisitDe(self, event, numDe):
        if self.deChoisi == -1 and not self.desJoues[numDe]:
            self.deChoisi = numDe

    def tour(self):
        """Fait le prochain tour"""
        if self.prochainJoueur == 0:
            nomJoueur = "blanc"
        else:
            nomJoueur = "noir"
        messagebox.showinfo("Prochain joueur",
                            "Joueur {}, c'est à vous !".format(nomJoueur))
        self.des = self.lancerDes()
        # AFFICHER LES DES
        for de in range(2):
            self.canvasDes[de].delete("all")
            self.canvasDes[de].create_image(
                50, 0, anchor="nw", image=self.imagesDes[self.des[de]-1])
        desJouables = [self.deEstJouable(
            self.prochainJoueur, de) for de in self.des]
        if desJouables == [False, False]:
            # Aucun dé n'est jouable
            messagebox.showinfo("Désolé !", "Aucun de vos dés n'est jouable !")
            self.desJoues = [True, True]
        else:
            for i in range(2):
                if not desJouables[i]:
                    # Si un des deux dés est non jouable, on dit qu'il est déjà joué
                    self.desJoues[i] = True
        # Sinon, on attend les events

    def jouer(self):
        """Lance le jeu"""
        while not self.termine() and not self.applicationQuittee:
            self.base.update()
            if self.desJoues == [True, True]:
                self.desJoues = [False, False]
                if self.prochainJoueur == 0:
                    self.prochainJoueur = 1
                else:
                    self.prochainJoueur = 0
                self.tour()
        # Partie finie
        if not self.applicationQuittee:
            for i in range(2):
                if self.aGagne(i):
                    champion = i
            if champion == 0:
                nomJoueur = "blanc"
            else:
                nomJoueur = "noir"
            messagebox.showinfo(
                "Bravo !", "Le joueur {} a gagné !".format(nomJoueur))
            self.tableauScore.vainqueur(champion, self.valeurPartie)
        self.tableauScore.base.deiconify()

    def rafraichirAffichage(self):
        """Recalcule l'affichage des pions"""
        self.canvas.delete("all")
        self.prisonCanvas.delete("all")
        for i in range(2):
            self.canvasDes[i].delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.imagePlateau)
        for i in range(24):
            for joueur in range(2):
                if joueur in self.jeu[i]:
                    nb = len(self.jeu[i])
                    x = self.casesPixels[i][0]
                    if i <= 11:
                        myAnchor = "nw"
                        y = self.casesPixels[i][2]
                    else:
                        myAnchor = "sw"
                        y = self.casesPixels[i][3]

                    self.canvas.create_image(
                        x, y, anchor=myAnchor, image=self.imagesPions[joueur][nb-1])
        for joueur in range(2):
            if self.prison.count(joueur) > 0:
                self.prisonCanvas.create_image(
                    0, 50*joueur, anchor="nw", image=self.imagesPionsPrison[joueur][self.prison.count(joueur)-1])
        for de in range(2):
            if self.desJoues[de]:
                self.canvasDes[de].create_image(
                    50, 0, anchor="nw", image=self.imagesDesGris[self.des[de]-1])
            else:
                self.canvasDes[de].create_image(
                    50, 0, anchor="nw", image=self.imagesDes[self.des[de]-1])
