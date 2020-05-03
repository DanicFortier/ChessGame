"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.

"""
from tkinter import NSEW, Canvas, Label, Tk, Button, Frame, messagebox
#from random import choice
import pickle

# Exemple d'importation de la classe Partie.
from pychecs2.echecs.partie import Partie

from  pychecs2.interface.Exceptions import AucunePieceAPosition, MauvaiseCouleurPiece, ErreurDeplacement, ProvoqueEchecJoueursActif

class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case, partie):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # La position sélectionnée.
        self.position_selectionnee = None

        self.partie = partie

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces. Vous devinerez, si vous réutilisez cette classe dans votre TP4,
        # qu'il faudra adapter ce code pour plutôt utiliser la classe Echiquier.
        self.pieces = {
            'a1': 'TB', 'b1': 'CB', 'c1': 'FB', 'd1': 'DB', 'e1': 'RB', 'f1': 'FB', 'g1': 'CB', 'h1': 'TB',
            'a2': 'PB', 'b2': 'PB', 'c2': 'PB', 'd2': 'PB', 'e2': 'PB', 'f2': 'PB', 'g2': 'PB', 'h2': 'PB',
            'a7': 'PN', 'b7': 'PN', 'c7': 'PN', 'd7': 'PN', 'e7': 'PN', 'f7': 'PN', 'g7': 'PN', 'h7': 'PN',
            'a8': 'TN', 'b8': 'CN', 'c8': 'FN', 'd8': 'DN', 'e8': 'RN', 'f8': 'FN', 'g8': 'CN', 'h8': 'TN',
        }

        self.correspondance_case_rectangle = {}

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.

        """

        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = 'white'
                else:
                    couleur = 'gray'  #couleur = self.ColorPalette.get_random_color

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.

                #Le clé permet d'identifier la case. La clé est simplement la postion: String
                key = self.lettres_colonnes[j] + self.chiffres_rangees[7 - i]

                self.correspondance_case_rectangle[key] = self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')


    def dessiner_pieces(self):
        # Caractères unicode représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        caracteres_pieces = {'PB': '\u2659',
                             'PN': '\u265f',
                             'TB': '\u2656',
                             'TN': '\u265c',
                             'CB': '\u2658',
                             'CN': '\u265e',
                             'FB': '\u2657',
                             'FN': '\u265d',
                             'RB': '\u2654',
                             'RN': '\u265a',
                             'DB': '\u2655',
                             'DN': '\u265b'
                             }

        # Pour tout paire position, pièce:
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text=piece,
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        self.rafraichir()

    def rafraichir(self):
       # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()


# class ColorPalette:
#     COLORS = [
#         "#39add1",  # Light Blue
#         "#3079ab",  # Dark Blue
#         "#c25975",  # Mauve
#         "#e15258",  # Red
#         "#f9845b",  # Orange
#         "#838cc7",  # Lavender
#         "#7d669e",  # Purple
#         "#53bbb4",  # Aqua
#         "#51b46d",  # Green
#         "#e0ab18",  # Mustard
#         "#637a91",  # Dark Gray
#         "#f092b0",  # Pink
#         "#b7c0c7"  # Light Gray
#     ]
#
#     @classmethod
#     def get_random_color(cls):
#         return choice(cls.COLORS)


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.fermeture)

        # Nom de la fenêtre.
        self.title("Échiquier")

        #Initialisation d'une partie
        self.partie = Partie()


        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie)
        self.canvas_echiquier.grid(sticky=NSEW)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Ajout d'une étiquette qui indique le joueur actif.
        self.messages_joueur_actif = Label(self)
        self.messages_joueur_actif['text'] = ("C'est au joueur blanc de commencer! ")
        self.messages_joueur_actif['foreground'] = 'blue'
        self.messages_joueur_actif.grid()

        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

        # Ajout d'un cadre pour regrouper les boutons
        frame_boutons = Frame(self)
        frame_boutons.grid(row=0, column=1)

        #Bouton pour annuler le dernier mouvement.
        bouton_dernier_mouvement = bouton_sauvegarder = Button(frame_boutons, text="Annuler le dernier mouvement", command=self.charger_dernier_mouvement)
        bouton_dernier_mouvement.grid()

        #Ajout des boutons pour sauvegarder et charger une partie.
        bouton_sauvegarder = Button(frame_boutons, text="Sauvegarder la partie", command=self.sauvegarder_partie)
        bouton_charger = Button(frame_boutons, text="Charger la partie", command=self.charger_partie)
        bouton_sauvegarder.grid()
        bouton_charger.grid()

        #Ajout d'un bouton pour commencer une nouvelle partie.
        bouton_nouvelle_partie = Button(frame_boutons, text="Nouvelle partie", command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid()

        #Ajout d'un bouton pour changer la couleur des cases grises dans le jeu.
        #bouton_change_couleur = Button(frame_boutons, text="Couleur thème", command=self.get_random_color)
        #bouton_change_couleur.grid()

    def fermeture(self):

        if messagebox.askyesno("Quitter", "Voulez vous sauvegarder la partie avant de quitter?"):
            self.sauvegarder_partie()

        self.destroy()

    def mise_a_jour_message_joueur_actif(self):
        self.messages_joueur_actif['foreground'] = 'blue'
        self.messages_joueur_actif['text'] = ("C'est le tour du joueur " + self.partie.joueur_actif + '.')

    def sauvegarder_partie(self):
        with open('./sauvegarde_partie.bin', 'wb') as f:
            pickle.dump(self.partie, f)

    def charger_partie(self):
        with open('./sauvegarde_partie.bin', 'rb') as f:
            try:
                self.canvas_echiquier.partie = pickle.load(f)

                self.partie = self.canvas_echiquier.partie

                self.canvas_echiquier.rafraichir()

                self.mise_a_jour_message_joueur_actif()

            except EOFError:
                self.messages['text'] = "Il n'y a pas de partie sauvegarder !"

    def sauvegarder_dernier_mouvement(self):
        with open('./dernier_mouvement.bin', 'wb') as f:
            pickle.dump(self.partie, f)

    def charger_dernier_mouvement(self):
        with open('./dernier_mouvement.bin', 'rb') as f:
            try:
                self.canvas_echiquier.partie = pickle.load(f)

                #C'est la chose la plus redneck que j'ai fait de toute ma vie
                self.partie = self.canvas_echiquier.partie

                self.canvas_echiquier.rafraichir()

                self.mise_a_jour_message_joueur_actif()


            except EOFError:
                self.messages['text'] = "Il n'y a pas de dernier mouvement !"


    def nouvelle_partie(self):
        self.canvas_echiquier.partie = Partie()
        self.partie = self.canvas_echiquier.partie

        self.canvas_echiquier.rafraichir()

        self.mise_a_jour_message_joueur_actif()
        self.messages['text'] = ""


    def premier_clic_valide(self, position):
        #Ceci permet au joueur actif de changer de pièce source sans compléter le déplacement.
        piece = self.partie.echiquier.recuperer_piece_a_position(position)

        if piece is None:
            raise AucunePieceAPosition('Aucune pièce à cet endroit!')
        elif piece.couleur != self.partie.joueur_actif:
            raise MauvaiseCouleurPiece("La pièce n'appartient pas au joueur " + self.partie.joueur_actif + '!')

    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))

        # Ce qui met en jaune c'est cette ligne-ci
        case = self.canvas_echiquier.correspondance_case_rectangle[position]
        self.canvas_echiquier.itemconfig(case, fill='yellow')

        self.sauvegarder_dernier_mouvement()




        try:
            if self.canvas_echiquier.position_selectionnee == None:

                # Puisque la pièce source est valide, on retire le message d'erreur actif
                self.messages['text'] = ""

                self.premier_clic_valide(position)

                #Premier clic: position_source
                self.canvas_echiquier.position_selectionnee = position


            else:
                # Condition qui permet de changer d'idée en cliquant sur une autre des pièces du joueur actif
                if self.partie.echiquier.couleur_piece_a_position(position) == self.partie.joueur_actif:

                    self.canvas_echiquier.rafraichir()
                    self.canvas_echiquier.position_selectionnee = position

                    case = self.canvas_echiquier.correspondance_case_rectangle[position]
                    self.canvas_echiquier.itemconfig(case, fill='yellow')



                else:
                    # Deuxième clic: position_cible
                    self.partie.deplacer(self.canvas_echiquier.position_selectionnee, position)
                    self.canvas_echiquier.position_selectionnee = None

                    # Detection echec
                    # Note: le joueur actif a changé
                    if self.partie.echiquier.echec_sur_le_roi_de_couleur(self.partie.joueur_actif):
                        self.messages['text'] = "Le roi " + self.partie.joueur_actif + " est en échec!"

                        #TODO: Échec et mat ici.
                        #if self.partie.echiquier.echec_et_mat_sur_le_roi_de_couleur(self.partie.joueur_actif):
                        #    self.messages['text'] = "Le roi " + self.partie.joueur_actif + " est en échec et mat!"



            if self.partie.partie_terminee():
                self.messages['foreground'] = 'green'
                self.messages['text'] = 'Partie terminée! Le joueur ' + self.partie.determiner_gagnant() + (' a gagné!')
            else:
                self.mise_a_jour_message_joueur_actif()






        except (ErreurDeplacement, AucunePieceAPosition, MauvaiseCouleurPiece) as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
            self.canvas_echiquier.position_selectionnee = None

        except ProvoqueEchecJoueursActif as e:
            self.messages['text'] = e
            self.charger_dernier_mouvement()
            self.canvas_echiquier.position_selectionnee = None


        finally:
            if self.canvas_echiquier.position_selectionnee == None:
                self.canvas_echiquier.rafraichir()



