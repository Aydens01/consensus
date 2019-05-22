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
import random as rd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from functools import partial

import consensus as css
####################################

#############| NOTES |##############
"""
FIXME: La matrice d'adjacence du graphe tous connectés 
       donne des résultats étranges.
"""
####################################

##########| CONSTANTES |############
"""
LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 500
POS_X_FENETRE = 300
POS_Y_FENETRE = 200
"""
LARGEUR_CANVAS = 600
HAUTEUR_CANVAS = 600
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
        self.Fenetre.attributes("-fullscreen", True)
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

        self.FrameButtons = tk.Frame(self.FrameOptionAjoutAgents,
                                     background = "#303030")

        self.ButtonRandom = tk.Button(self.FrameButtons,
                                      text = "Aléatoire",
                                      padx=30,
                                      foreground="#FFFFFF",
                                      activebackground="#303030",
                                      background = "#303030",
                                      command = partial(self.genRandomly))
        
        self.ButtonDelAll = tk.Button(self.FrameButtons,
                                      text = "Supprimer tout",
                                      padx=30,
                                      foreground="#FFFFFF",
                                      activebackground="#303030",
                                      background = "#303030",
                                      command=partial(self.suppAll))

        
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

            # * Frame Matrice d'adjacence
        self.FrameAdjacence = tk.LabelFrame(self.FrameOptionAjoutAgents,
                                            text="Choix du graphe",
                                            background="#303030",
                                            foreground="#FFFFFF",
                                            padx=10, pady=10)

        self.adjacence = tk.IntVar()
        self.adjacence.set(0)

        self.RadioAdja0 = tk.Radiobutton(self.FrameAdjacence,
                                         text = "Tous connectés",
                                         indicatoron=0,
                                         variable = self.adjacence,
                                         value = 0)
        
        self.RadioAdja1 = tk.Radiobutton(self.FrameAdjacence,
                                         text = "Un leader",
                                         indicatoron=0,
                                         variable = self.adjacence,
                                         value = 1)
        
        self.RadioAdja2 = tk.Radiobutton(self.FrameAdjacence,
                                         text = "En ligne",
                                         indicatoron=0,
                                         variable = self.adjacence,
                                         value = 2)

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
                                   pady=10, padx=10)

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

            # * Frame Temps
        self.FrameTemps = tk.LabelFrame(self.FrameGauche,
                                        text = "Simulation",
                                        background="#303030",
                                        foreground="#FFFFFF",
                                        padx=10, pady=10)
        
        self.LabelT = tk.Label(self.FrameTemps,
                               text = "Période [0,T] (entrez T)",
                               pady=5,
                               background="#303030",
                               foreground="#FFFFFF")
        
        self.EntryT = tk.Entry(self.FrameTemps,
                               text = tk.StringVar(self.FrameTemps))

        self.LabelN = tk.Label(self.FrameTemps,
                               text = "Nombre d'itérations",
                               pady=5,
                               background="#303030",
                               foreground="#FFFFFF")
        
        self.EntryN = tk.Entry(self.FrameTemps,
                               text = tk.StringVar(self.FrameTemps))

            # * Frame Option Go 
        self.FrameOptionGo = tk.Frame(self.FrameGauche,
                                      background="#303030",
                                      pady="10")
        
        self.BoutonLancement = tk.Button(self.FrameOptionGo,
                                         text = "Démarrer",
                                         padx=50,
                                         foreground="#FFFFFF",
                                         activebackground="#303030",
                                         background = "#303030",
                                         command = partial(self.go))
        
        self.BoutonArret = tk.Button(self.FrameOptionGo,
                                     text="Arrêter",
                                     padx=50,
                                     foreground="#FFFFFF",
                                     activebackground="#303030",
                                     background = "#303030")
                                     # TODO: command = partial()

        # * Canvas
        self.Canvas = tk.Canvas(self.FrameCanvas,
                                background = "#4C4C4C",
                                width = LARGEUR_CANVAS, 
                                height = HAUTEUR_CANVAS)
        
        self.FrameCanvasBot = tk.Frame(self.FrameCanvas,
                                       background="#303030")
            # * Frame Load
        self.FrameLoad = tk.LabelFrame(self.FrameCanvasBot,
                                       text = "Charger un fichier (.txt)",
                                       background="#303030",
                                       foreground="#FFFFFF",
                                       padx = 10, pady = 10)
        
        self.EntryLoad = tk.Entry(self.FrameLoad,
                                  text = tk.StringVar(self.FrameLoad))
        
        self.BoutonLoad = tk.Button(self.FrameLoad,
                                    text = "Charger",
                                    padx=50,
                                    foreground="#FFFFFF",
                                    activebackground="#303030",
                                    background = "#303030")
                                    # todo: command = partial()
            # * Frame Save
        self.FrameSave = tk.LabelFrame(self.FrameCanvasBot,
                                       text = "Sauvegarder le système",
                                       background="#303030",
                                       foreground="#FFFFFF",
                                       padx = 10, pady = 10)
        
        self.EntrySave = tk.Entry(self.FrameSave,
                                  text = tk.StringVar(self.FrameSave))
        
        self.BoutonSave = tk.Button(self.FrameSave,
                                    text = "Sauver",
                                    padx=50,
                                    foreground="#FFFFFF",
                                    activebackground="#303030",
                                    background = "#303030")
                                    # todo: command = partial()

        # * Graphe
        self.FrameGraph = tk.LabelFrame(self.Fenetre,
                                        labelanchor='n',
                                        text="Graphe",
                                        borderwidth="2",
                                        padx=5, pady=0,
                                        background="#303030",
                                        foreground="#FFFFFF")

            # * Création du graphe
        self.Figure = Figure(figsize=(5,5), dpi=100)
        self.Graph = FigureCanvasTkAgg(self.Figure, self.FrameGraph)
        self.Graph.draw()

        self.Toolbar = NavigationToolbar2Tk(self.Graph, self.FrameGraph)
        self.Toolbar.update()


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

        self.FrameCoord.grid(column=0, row=1)
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

        self.FrameAdjacence.grid(column=0, row=2)
        self.RadioAdja0.grid(column=0, row=0)
        self.RadioAdja1.grid(column=1, row=0)
        self.RadioAdja2.grid(column=2, row=0)

        self.FrameButtons.grid(column=0, row=3)
        self.ButtonRandom.grid(column=0, row=0, pady=10)
        self.ButtonDelAll.grid(column=1, row=0, pady=10)
        
        self.FrameTemps.grid(column=0, row=1, sticky='n')
        self.LabelT.grid(column=0, row=0)
        self.LabelN.grid(column=1, row=0)
        self.EntryT.grid(column=0, row=1)
        self.EntryN.grid(column=1, row=1)

        self.FrameOptionGo.grid(column=0, row=2, sticky='n')
        self.BoutonLancement.grid(column=0, row=0, sticky='nswe')
        self.BoutonArret.grid(column=1, row=0, sticky='nswe')

        self.FrameCanvas.grid(column=1, row=0)
        self.Canvas.grid(column=0, row=0)
        self.FrameCanvasBot.grid(column=0, row=1)
        self.FrameLoad.grid(column=0, row=0)
        self.EntryLoad.grid(column=0, row=0, padx=5)
        self.BoutonLoad.grid(column=1, row=0, padx=5)

        self.FrameSave.grid(column=1, row=0)
        self.EntrySave.grid(column=0, row=0, padx=5)
        self.BoutonSave.grid(column=1, row=0, padx=5)

        self.FrameGraph.grid(column=2, row=0, sticky='n')
        self.Graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.Graph._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # * Binds
        self.Canvas.bind('<Button-1>', partial(self.fonctionClicGauche))
        self.Fenetre.bind("<F11>", self.toggle_fullscreen)
        self.Fenetre.bind("<Escape>", self.end_fullscreen)
    
    def toggle_fullscreen(self, event=None):
        self.Fenetre.attributes("-fullscreen", True)
    
    def end_fullscreen(self, event=None):
        self.state = False
        self.Fenetre.attributes("-fullscreen", False)

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
        color = ["#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF"]
        for i in range(len(self.agents)):
            X = self.agents[i].params[0]
            Y = self.agents[i].params[1]
            self.Canvas.create_oval(X-5, Y-5, X+5, Y+5, fill=color[i] if i <7 else color[0])

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
            self.agents.append(css.Agent(4, [], np.array([float(pos_x), float(pos_y),rd.randint(-20, 20),rd.randint(-20, 20)])))
            # On actualise le Canvas
            self.affichage()
        else:
            #TODO: ajout obstacle
            pass

    def suppAll(self):
        """ Réinitialise le Canvas et supprime tous les éléments
        """
        self.agents = []
        self.obstacles = []
        self.affichage()


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

    def genMadjacence(self):
        """ Génère la matrice d'adjacence du graphe choisi
        par l'utilisateur
        """
        nb_agents = len(self.agents)
        if self.adjacence.get()==0:
            output = np.array([ [1 if i!=k else 0 for i in range(nb_agents)] for k in range(nb_agents)])
        elif self.adjacence.get()==1:
            output = np.array([ [1 if k!=1 else 0 for i in range(nb_agents)] for k in range(nb_agents)])
        elif self.adjacence.get()==2:
            output = np.array([ [1 if k-1==i or k+1==i else 0 for i in range(nb_agents)] for k in range(nb_agents)])
        return(output)

    def loop(self, sys, index):
        """ Effectue les déplacements des agents sur le 
        Canvas pour une itération
        """
        status = sys.consensus[index]
        for k in range(len(self.agents)):
            self.agents[k].params[0] = status[k*4]
            self.agents[k].params[1] = status[k*4+1]
        # On actualise le Canvas
        self.affichage()

        if index<len(sys.consensus)-1:
            self.Canvas.after(100, self.loop, sys, index+1)

    def go(self):
        """ Animation des agents vers le consensus 
        """
        T = self.EntryT.get()
        N = self.EntryN.get()

        check = self.verifSaisie([T, N])

        if check:
            madjacence = self.genMadjacence()
            # Résolution du consensus
            sys = css.System(self.agents, float(T)/float(N), float(T), madjacence)
            # On réinitilise le graphe
            self.Figure.clear()
            self.ax = self.Figure.add_subplot(111)
            t = np.arange(0,sys.loss.shape[0])
            for i in range(sys.loss.shape[1]):
                data = [sys.loss[j][i] for j in range(sys.loss.shape[0])]
                self.ax.plot(t, data, marker='', color='black', linewidth=1)
            
            self.Graph.draw()
            self.Toolbar.update()
            self.loop(sys, 0)

        else:
            print("Erreur : Données d'entrée invalides")

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
    