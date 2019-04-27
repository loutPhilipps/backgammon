# -------------------------------------------------------------------------------

from tkinter import *
from random import *

base = Tk()
base.title("Backgammon")

# importer image plateau
canvas = Canvas(base)
canvas.pack(fill=X)


photo = PhotoImage(file="plateau.png")
canvas.create_image(100, 80, image=photo)


# boutton pour quitter
boutton = Button(base, text="Quitter", command=base.destroy)
boutton.pack(side=BOTTOM)

# boutton pour reinitialiser
boutton = Button(base, text="reinitialiser", command=base)
boutton.pack(side=BOTTOM)


# boutton pour sauvegarder
boutton = Button(base, text="sauvegarder", command=base)
boutton.pack(fill=X)


# boutton score des joueurs
boutton = Checkbutton(base, text="score joueur a", command=base, indicatoron=0)
boutton.pack(side=LEFT)
boutton = Checkbutton(base, text="score joueur b", command=base, indicatoron=0)
boutton.pack(side=LEFT)

# boutton pari
choix_bleu = Checkbutton(base, text="pari?", command=base, indicatoron=1)
choix_bleu.pack(side=TOP)

# boutton pour lancer de
boutton = Button(base, text="lancement de", command=base)
boutton.pack(fill=X)


# boucle principale
base.mainloop()

# lancement du de


def lancement2de():  # creation 2 des
    de1 = randint(1, 6)  # retour entier aleatoire entre 1 et 6
    de2 = randint(1, 6)

    lancer = de1 + de2

    if de1 == 1:  # affichage de par rapport resulat de1
        un()
    elif de1 == 2:
        deux()
    elif de1 == 3:
        trois()
    elif de1 == 4:
        quatre()
    elif de1 == 5:
        cinq()
    elif de1 == 6:
        six()

    if de2 == 1:  # affichage de par rapport resulat de2
        un()
    elif de2 == 2:
        deux()
    elif de2 == 3:
        trois()
    elif de2 == 4:
        quatre()
    elif de2 == 5:
        cinq()
    elif de2 == 6:
        six()

    return lancer


def un():
    print("----------")  # changer en image
    print("|        |")
    print("|    *   |")
    print("|        |")
    print("----------")


def deux():
    print("----------")
    print("| *       |")
    print("|         |")
    print("|       * |")
    print("-----------")


def trois():
    print("----------")
    print("| *       |")
    print("|    *    |")
    print("|       * |")
    print("-----------")


def quatre():
    print("----------")
    print("| *     * |")
    print("|         |")
    print("| *     * |")
    print("-----------")


def cinq():
    print("----------")
    print("| *     * |")
    print("|    *    |")
    print("| *     * |")
    print("-----------")


def six():
    print("----------")
    print("|  *   *  |")
    print("|  *   *  |")
    print("|  *   *  |")
    print("-----------")


print("appuyer sur\"entrer\" pour lancer les des")
input()
monlancer = lancement2de()
print("vous avez fait " + str(monlancer))
