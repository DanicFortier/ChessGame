# -*- coding: utf-8 -*-
"""Module principal du package pychecs2. C'est ce module que nous allons exécuter pour démarrer votre jeu.
Importez les modules nécessaires et démarrez votre programme à partir d'ici. Le code fourni n'est qu'à titre d'exemple.

"""
from pychecs2.echecs.partie import Partie
from pychecs2.interface.interface import Fenetre

if __name__ == '__main__':

    # Création et affichage d'une fenêtre.
    f = Fenetre()

    f.mainloop()
