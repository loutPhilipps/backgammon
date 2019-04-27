# -------------------------------------------------------------------------------
# Projet Backgammon
# -------------------------------------------------------------------------------

# Conventions :
# - noirs: 1, sort en 23
# - blancs: 0, sort en 0

import random


class Backgammon:
    def __init__(self):
        """Création d'un jeu de backgammon"""
        self.jeu = [[] for i in range(24)]
        self.remplirInitial()
        self.prison = []
        self.prochainJoueur = random.randint(0, 1)

    def remplirInitial(self):
        """Place les pions au départ"""
        self.jeu[0] = [1, 1]
        self.jeu[5] = [0, 0, 0, 0, 0]
        self.jeu[7] = [0, 0, 0]
        self.jeu[11] = [1, 1, 1, 1, 1]
        self.jeu[12] = [0, 0, 0, 0, 0]
        self.jeu[16] = [1, 1, 1]
        self.jeu[18] = [1, 1, 1, 1, 1]
        self.jeu[23] = [0, 0]

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

    def des(self):
        return (random.randint(1, 6), random.randint(1, 6))

    def deplacement(self, joueur, valeurDe, case):
        """deplacement des pions noir et blancs"""
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

    def aGagne(self, joueur):
        """Verifie si le joueur a gagne"""
        for case in self.jeu:
            if joueur in case:
                return False
        return True

    def termine(self):
        """Verifie si le jeu est termine"""
        for joueur in range(2):
            if self.aGagne(joueur):
                return True
        return False

    def choisirCase(self, de):
        """Verifie que le joueur choisit une case jouable"""
        bonneCase = False
        while not bonneCase:
            caseChoisie = input(
                "Entrez le numero de case ou vous voulez jouer (-1 pour la prison)")
            if caseChoisie not in [str(i) for i in range(-1, 24)]:
                print("Non !")
            elif not self.verifierDeplacement(self.prochainJoueur, de, int(caseChoisie)):
                print("Vous n'avez pas le droit de faire ce deplacement")
            else:
                bonneCase = True
        return int(caseChoisie)

    def choisirDe(self):
        """Choisir entre 0 et 1"""
        deChoisi = input("Choisissez votre de (0 ou 1)")
        while deChoisi not in ["0", "1"]:
            print("Mauvaise valeur de de")
            deChoisi = input("Choisissez votre de (0 ou 1)")
        return int(deChoisi)

    def tour(self):
        """Fait le prochain tour"""
        if self.prochainJoueur == 0:
            nomJoueur = "blanc"
        else:
            nomJoueur = "noir"
        print("Joueur {}, c'est a  vous !".format(nomJoueur))
        des = self.des()
        print("Vous avez fait {} et {}".format(des[0], des[1]))
        desJouables = [self.deEstJouable(
            self.prochainJoueur, de) for de in des]
        if desJouables != [False, False]:
            # Au moins un de est jouable
            print("Voici l'etat du jeu :")
            print(self.jeu, self.prison)
            deChoisi = self.choisirDe()
            if desJouables[deChoisi]:
                caseChoisie = self.choisirCase(des[deChoisi])
                self.deplacement(self.prochainJoueur,
                                 des[deChoisi], caseChoisie)
            else:
                print("Ce de n'est pas jouable !")
            if deChoisi == 1:
                autreDe = 0
            else:
                autreDe = 1
            print("La valeur du de restant est {}".format(des[autreDe]))
            if desJouables[autreDe]:
                print(self.jeu, self.prison)
                caseChoisie = self.choisirCase(des[deChoisi])
                self.deplacement(self.prochainJoueur,
                                 des[deChoisi], caseChoisie)
            else:
                print("Ce de n'est pas jouable")
        if self.aGagne(self.prochainJoueur):
            print("Vous avez gagne !")
        else:
            print("Fin du tour du joueur {}".format(nomJoueur))
        if self.prochainJoueur == 0:
            self.prochainJoueur = 1
        else:
            self.prochainJoueur = 0

    def jouer(self):
        """Lance le jeu"""
        while not self.termine():
            self.tour()
