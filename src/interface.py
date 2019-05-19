#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
auteur  : Prénom Nom \n
date    : 03.19
Fichier type (Titre)
=============
Description de ce qu'apporte le fichier
    1. ...
    2. ...

...
"""

############| IMPORTS |#############
import os
import sys
sys.path.append('../src/lib')

import numpy as np

import tkinter as tk
import tkinter.ttk as ttk

from functools import partial

import consensus as css
####################################

#############| NOTES |##############
"""
TODO:
"""
####################################

##########| CONSTANTES |############
LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 500
POS_X_FENETRE = 300
POS_Y_FENETRE = 200

LARGEUR_CANVAS = LARGEUR_FENETRE - 230
HAUTEUR_CANVAS = HAUTEUR_FENETRE - 25
####################################


class Interface():

    def  __init__(self):
        self.Fenetre = tk.Tk()
        self.agents = []
        self.obstacles = []
        self.initialisation()
    
    def initialisation(self):
        """ Initialise la fenêtre tkinter et les differentes
            variables liées à celle-ci
        """
        # * Général
        self.Fenetre.title("Consensus")
        """
        self.Fenetre.geometry("%sx%s+%s+%s" % (LARGEUR_FENETRE,
                                              HAUTEUR_FENETRE,
                                              POS_X_FENETRE,
                                              POS_Y_FENETRE))
        """
        self.Fenetre.configure(background="#303030")

        # * Fenetre
        self.FrameGauche = tk.LabelFrame(self.Fenetre,
                                         labelanchor = "n",
                                         text = "Options",
                                         borderwidth = "2",
                                         padx=5, pady=0,
                                         background="#303030",
                                         foreground="#FFFFFF")

        self.FrameCanvas = tk.LabelFrame(self.Fenetre,
                                         labelanchor="n",
                                         text = "Canvas",
                                         borderwidth="2",
                                         padx=0, pady=0,
                                         background="#303030",
                                         foreground="#FFFFFF")

        # * Frame Gauche
        
        self.FrameOptionAjoutAgents = tk.LabelFrame(self.FrameGauche,
                                               labelanchor="n",
                                               text = "Ajout d'éléments",
                                               borderwidth = "2",
                                               padx=10, pady=10,
                                               background="#303030",
                                               foreground="#FFFFFF")
            # * Frame Option Ajout Agent
        self.FrameOptionHead = tk.Frame(self.FrameOptionAjoutAgents,
                                        background="#303030")
        
        self.FrameAgentObstacle = tk.LabelFrame(self.FrameOptionHead,
                                                text = "Type",
                                                background="#303030",
                                                foreground="#FFFFFF",
                                                pady=10, padx=10)

        self.ButtonRandom = tk.Button(self.FrameOptionAjoutAgents,
                                      text = "Aléatoire",
                                      padx=30,
                                      foreground="#FFFFFF",
                                      activebackground="#303030",
                                      background = "#303030",
                                      command = partial(self.genRandomly))
                                      # TODO:
        
        self.agentObstacle = tk.BooleanVar()
        self.agentObstacle.set(True)
                # * Frame Agent Obstacle
        self.RadioAgent = tk.Radiobutton(self.FrameAgentObstacle,
                                         text = "Agents", 
                                         indicatoron=0,
                                         variable = self.agentObstacle,
                                         value = True)
        
        self.RadioObstacle = tk.Radiobutton(self.FrameAgentObstacle,
                                            text = "Obstacles",
                                            indicatoron = 0,
                                            variable = self.agentObstacle,
                                            value = False)
                # * Frame Nb Agent
        self.FrameNbAgent = tk.Frame(self.FrameOptionHead,
                                     background="#303030",
                                     pady=10, padx=10)

        self.LabelNbAgent = tk.Label(self.FrameNbAgent,
                                     text = "Nombre d'agents : ",
                                     pady = 5,
                                     background="#303030",
                                     foreground="#FFFFFF")
        
        self.EntryNbAgent = tk.Entry(self.FrameNbAgent,
                                     text = tk.StringVar(self.FrameOptionHead))
                # * Frame Coordonnées
        self.FrameCoord = tk.LabelFrame(self.FrameOptionAjoutAgents,
                                   text = "Coordonnées",
                                   background="#303030",
                                   foreground="#FFFFFF",
                                   pady="10", padx="10")

        self.FrameForm = tk.Frame(self.FrameCoord,
                                  background="#303030")

        #!######### FORMULAIRE ########## # TODO: Partie dynamique

        #// if self.cas == 2d

        self.LabelP_X = tk.Label(self.FrameForm,
                                 text = "Position (axe x)",
                                 pady = 5,
                                 background="#303030",
                                 foreground="#FFFFFF")

        self.EntryP_X = tk.Entry(self.FrameForm,
                                 text = tk.StringVar(self.FrameForm))

        self.LabelP_Y = tk.Label(self.FrameForm,
                                 text = "Position (axe y)",
                                 pady = 5,
                                 background="#303030",
                                 foreground="#FFFFFF")

        self.EntryP_Y = tk.Entry(self.FrameForm,
                                 text = tk.StringVar(self.FrameForm))

        self.LabelV_X = tk.Label(self.FrameForm,
                                 text = "Vitesse (axe x)",
                                 pady = 5,
                                 background="#303030",
                                 foreground="#FFFFFF")

        self.EntryV_X = tk.Entry(self.FrameForm,
                                 text = tk.StringVar(self.FrameForm))

        self.LabelV_Y = tk.Label(self.FrameForm,
                                 text = "Vitesse (axe y)",
                                 pady = 5,
                                 background="#303030",
                                 foreground="#FFFFFF")
        
        self.EntryV_Y = tk.Entry(self.FrameForm,
                                 text = tk.StringVar(self.FrameForm))
        
        #!########## FORMULAIRE ##########

        self.ButtonAjouter = tk.Button(self.FrameCoord,
                                       text = "Ajouter",
                                       padx=50,
                                       foreground="#FFFFFF",
                                       activebackground="#303030",
                                       background = "#303030",
                                       command=partial(self.ajout))

        self.ButtonSupprimer = tk.Button(self.FrameCoord,
                                         text = "Annuler",
                                         padx=50,
                                         foreground="#FFFFFF",
                                         activebackground="#303030",
                                         background = "#303030",
                                         command=partial(self.supprime))

            # * Frame Option Go 
        self.FrameOptionGo = tk.Frame(self.FrameGauche,
                                           background="#303030",
                                           pady="10")
        
        self.BoutonLancement = tk.Button(self.FrameOptionGo,
                                         text = "GO !",
                                         padx=70,
                                         foreground="#FFFFFF",
                                         activebackground="#303030",
                                         background = "#303030")
                                         #TODO: command=partial()

        # * Canvas
        self.Canvas = tk.Canvas(self.FrameCanvas,
                                background = "#4C4C4C",
                                width = LARGEUR_CANVAS, 
                                height = HAUTEUR_CANVAS)
        
        # * Design de la Fenetre
        self.FrameGauche.grid(column=0, row=0, sticky='n')

        self.FrameOptionAjoutAgents.grid(column=0, row=0, sticky='n')
        self.FrameOptionHead.grid(column=0, row=0)
        self.FrameAgentObstacle.grid(column=0, row=0)
        self.FrameNbAgent.grid(column=1, row=0)

        self.RadioAgent.grid(column=0, row=0, sticky= 'w', padx= 20)
        self.RadioObstacle.grid(column=1, row=0, sticky= 'w', padx= 20)
        self.LabelNbAgent.grid(column = 1, row=0)
        self.EntryNbAgent.grid(column=1, row = 1)

        self.FrameCoord.grid(column=0, row=2)
        self.FrameForm.grid(column=0, row=0)
        self.LabelP_X.grid(column=0, row=0)
        self.LabelP_Y.grid(column=1, row=0)
        self.EntryP_X.grid(column=0, row=1)
        self.EntryP_Y.grid(column=1, row=1)
        self.LabelV_X.grid(column=0, row=2)
        self.LabelV_Y.grid(column=1, row=2)
        self.EntryV_X.grid(column=0, row=3)
        self.EntryV_Y.grid(column=1, row=3)
        self.ButtonAjouter.grid(column=0, row=1, pady=10, sticky='nswe')
        self.ButtonSupprimer.grid(column=0, row=2, sticky='nswe')

        self.ButtonRandom.grid(column=0, row=3, pady=10)

        self.FrameOptionGo.grid(column=0, row=1, sticky='n')
        self.BoutonLancement.grid(column=0, row=0, sticky='nswe')

        self.FrameCanvas.grid(column=1, row=0)
        self.Canvas.grid(column=0, row=0)

        # * Binds
        self.Canvas.bind('<Button-1>', partial(self.fonctionClicGauche))

    def verifSaisie(self, valeurs):
        """ Retourne : 1 si le nombre entré est un réel
        """
        for valeur in valeurs:
            try: 
                float(valeur)
            except ValueError:
                return(False)
        
        return(True)

    def affichage(self):
        """Affiche le système sur le canvas
        """
        # On réinitialise le Canvas
        self.Canvas.delete("all")
        for agent in self.agents:
            X = agent.params[0]
            Y = agent.params[1]
            self.Canvas.create_oval(X-5, Y-5, X+5, Y+5, fill="#FFFFFF")

    def ajout(self):
        """ Ajoute des agents ou des obstacles
        """
        pos_x = self.EntryP_X.get() 
        pos_y = self.EntryP_Y.get()
        vit_x = self.EntryV_X.get()
        vit_y = self.EntryV_Y.get()

        check = self.verifSaisie([pos_x, pos_y, vit_x, vit_y])

        if check :
            if self.agentObstacle.get()==True:
                params = np.array([float(pos_x), float(pos_y), float(vit_x), float(vit_y)])
                self.agents.append(css.Agent(4, [], params))
                # On actualise le Canvas
                self.affichage()
            else :
                #TODO: ajout un obstacle
                pass
        else :
            print("Erreur : Données d'entrée invalides !")

    def supprime(self):
        """ Supprime le dernier élément ajouté
        """
        if self.agentObstacle.get()==True:
            try:
                del self.agents[-1]
                # On actualise le Canvas
                self.affichage()

            except IndexError:
                print("Erreur : Il n'y a aucun agent à supprimer !")
    
    def fonctionClicGauche(self, event):
        """ Ajoute un agent sur le canvas à l'endroit de la souris
        """
        # Position souris
        pos_x = event.x
        pos_y = event.y

        if self.agentObstacle.get()==True:
            # On ajoute un nouvel agent à la liste
            self.agents.append(css.Agent(4, [], np.array([float(pos_x), float(pos_y),0,0])))
            # On actualise le Canvas
            self.affichage()
        else:
            #TODO: ajout obstacle
            pass

    def genRandomly(self):
        """ Génère les agents aléatoirement
        """
        nb_agents = self.EntryNbAgent.get()

        if self.verifSaisie([nb_agents]):
            if self.agentObstacle.get()==True:
                self.agents = [css.Agent(4, [100, 400]) for i in range(int(nb_agents))]
                # On actualise le Canvas
                self.affichage()
            else:
                #TODO: génération aléatoire d'obstacles
                pass
        pass

    def go(self):
        """ Animation des agents vers le consensus 
        """
        pass

    def main(self):
        """ Lance l'interface
        """
        self.Fenetre.mainloop()

####################################
############| PROGRAM |#############
####################################

if __name__=="__main__" :
    # Environnement de test (provisoire)
    app = Interface()
    app.main()
    