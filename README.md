# Projet Backgammon - Adam Philipps

## Prérequis

Il vous faut Python 3, ainsi que les modules `tkinter` et `pillow`.
Vous pouvez installer PIL en lançant `python -m pip install pillow` dans la ligne de commande Windows (invite de commandes).

## Lancer le projet

Vérifiez que vous avez bien python avec tkinter d'installé.
Executez ensuite le fichier `main.py`.

## Objectifs du projets

Les objectifs du projet étaient les suivants:

- création d'un _backgammon_
- création d'une _interface graphique_
- jouable en _Joueur contre Joueur_
- éventuellement, jouable en _Joueur contre ordinateur_
- pouvoir _rejouer_, _réinitialiser_ ou _quitter_ la partie
- éventuellement, pouvoir _sauvegarder_ une partie en cours
- éventuellement, implémenter certaines règles optionnelles (_paris_ notamment)
- éventuellement, gestion des _scores_ (plusieurs parties)

## Participants au projet

- Adam PHILIPPS

## Explication rapide du fonctionnement

- Le coeur du fonctionnement du programme est situé dans la classe `Backgammon` du fichier `backgammon.py`.
- Le fichier `affichage.py` gère l'affichage graphique du jeu.
- Le fichier `main.py` lance simplement le Lanceur du jeu.
