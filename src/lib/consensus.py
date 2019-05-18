#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
auteur  : Adrien Lafage \n
date    : 05.19
Consensus
=============
Description de ce qu'apporte le fichier
    1. ...
    2. ...

...
"""

############| IMPORTS |#############
import os
import sys
import numpy as np
import random as rd
import matplotlib.pyplot as plt
####################################

#############| NOTES |##############
"""
TODO:
"""
####################################

class Agent():
    """ Modélisation d'un agent"""

    id = 0

    def __init__(self, nb_param):
        """ Initialisation de l'agent
        Paramètres :
        ------------
            nb_param {int} : nombre de coordonnées de l'agent
        """
        self.id = Agent.id
        Agent.id += 1
        self.nb_param = nb_param
        self.params = self.gen()
    
    def gen(self) :
        """ Génère aléatoirement les paramètres de l'agent
        Paramètres :
        ------------
            nb_param {int} : nombre de coordonnées de l'agent
        Sortie :
        --------
            output {np.array}
        """
        output = np.array([rd.randint(1, 5) for k in range(self.nb_param)])
        return(output)
    
    def __repr__(self):
        """ Fonction d'affichage de l'agent
        """
        output = "Agent\n"
        for k in range(self.nb_param):
            output += "param"+str(k+1)+" : " + str(self.params[k])+"\n"
        return(output)


class System():
    """Système d'agents"""
    def __init__(self, agents, pas, temps, alpha=1):
        """ Initialisation du système
        Paramètres :
        ------------
            agents {Agent list} : La liste des agents
        """
        self.pas = pas
        self.temps = temps
        self.alpha = alpha if 0<alpha<=1 else 1
        self.init_matrice = self.normalize(agents)
        self.mtransition = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [-2, 0, -2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                     [0, -2, 0, -2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [1, 0, 1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 1, 0, 1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [1, 0, 1, 0, 0, 0, 0, 0, -2, 0, -2, 0, 1, 0, 1, 0],
                                     [0, 1, 0, 1, 0, 0, 0, 0, 0, -2, 0, -2, 0, 1, 0, 1],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, -1, 0, -1, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, -1, 0, -1]])
        self.consensus = self.euler()

    def normalize(self, agents):
        """ Initialise le vecteur X contenant l'ensemble des agents
        à l'instant 0.
        Paramètres :
        ------------
            agents {Agent list} : La liste des agents du système
        Sortie :
        --------
            output {np.array}
        """
        output = np.array([])
        for a in agents:
            for param in a.params:
                output = np.append(output, np.array([param]))
        return(output)

    def phi_alpha(self, X):
        """ Applique la fonction Phi au vecteur du système
        Paramètres :
        ------------
            X {np.array} : vecteur du système
        Sortie :
            output {np.array}
        """
        output = np.zeros(X.size)
        for i in range(1, X.size+1):
            if (i%4==3) or (i%4==0) :
                output[i-1] = np.sign(X[i-1])*abs(X[i-1]**self.alpha)
            else:
                output[i-1] = X[i-1]
        return(output)

    def euler(self):
        """ Méthode d'Euler pour approcher le consensus
        entre les agents
        """
        t = 0
        N = int(self.temps/self.pas)+2
        output = np.zeros((N, 16))
        output[0] = self.init_matrice
        n = 1
        while t<self.temps:
            Z = self.pas*self.phi_alpha(np.dot(self.mtransition,output[n-1]))
            output[n] = output[n-1]+Z
            t += self.pas
            n+=1
        return(output)
    
    def show(self):
        """ Affiche le graphe représentant le système
        # ! Non modulable, marche uniquement pour 4 agents
        # ! dont les positions selon x et y sont leurs deux 
        # ! premiers paramètres
        """
        axis_x_agent1 = [state[0] for state in self.consensus]
        axis_y_agent1 = [state[1] for state in self.consensus]

        axis_x_agent2 = [state[4] for state in self.consensus]
        axis_y_agent2 = [state[5] for state in self.consensus]

        axis_x_agent3 = [state[8] for state in self.consensus]
        axis_y_agent3 = [state[9] for state in self.consensus]

        axis_x_agent4 = [state[12] for state in self.consensus]
        axis_y_agent4 = [state[13] for state in self.consensus]

        plt.plot(axis_x_agent1, axis_y_agent1, 'r*') 
        plt.plot(axis_x_agent2, axis_y_agent2, 'b*')
        plt.plot(axis_x_agent3, axis_y_agent3, 'g*')
        plt.plot(axis_x_agent4, axis_y_agent4, 'm*')
        plt.show()


####################################
############| PROGRAM |#############
####################################

if __name__=="__main__" :
    # Environnement de test (provisoire)
    agents = [Agent(4) for i in range(4)]
    sys = System(agents, pas=0.1, temps=5)
    #//print(sys.consensus)
    sys.show()