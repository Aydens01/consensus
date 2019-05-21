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
TODO
"""
####################################

class Agent():
    """ Modélisation d'un agent"""

    id = 0

    def __init__(self, nb_params, intervalle=[1, 20], params=np.array([])):
        """ Initialisation de l'agent
        Paramètres :
        ------------
            nb_param {int} : nombre de coordonnées de l'agent
        """
        self.id = Agent.id
        Agent.id += 1
        self.nb_params = nb_params
        self.int = intervalle
        # ! check that
        self.params = self.gen() if nb_params!=params.size else params
    
    def gen(self) :
        """ Génère aléatoirement les paramètres de l'agent
        Paramètres :
        ------------
            nb_param {int} : nombre de coordonnées de l'agent
        Sortie :
        --------
            output {np.array}
        """
        a, b = self.int[0], self.int[1]

        output = np.array([rd.randint(a, b), rd.randint(a, b), rd.randint(-20, 20), rd.randint(-20, 20)])
        return(output)
    
    def __repr__(self):
        """ Fonction d'affichage de l'agent
        """
        output = "Agent\n"
        for k in range(self.nb_params):
            output += "param"+str(k+1)+" : " + str(self.params[k])+"\n"
        return(output)


class System():
    """Système d'agents"""
    def __init__(self, agents, pas, temps, madjacence, alpha=1):
        """ Initialisation du système
        Paramètres :
        ------------
            agents {Agent list} : La liste des agents
        """
        self.pas = pas
        self.temps = temps
        self.alpha = alpha if 0<alpha<=1 else 1
        self.agents = agents
        self.init_matrice = self.normalize(agents)
        self.madjacence = madjacence
        self.consensus = self.euler()
        self.loss = self.lossFct()

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

    def deriv(self, vect):
        output = np.array([])
        for k in range(len(self.agents)):
            agent = np.array([vect[k*4+i] for i in range(2,4)])
            u1 = 0
            u2 = 0
            for j in range(len(self.agents)):
                u1+=self.madjacence[k][j]*((vect[k*4]-vect[j*4])+(vect[k*4+2]-vect[j*4+2]))
                u2+=self.madjacence[k][j]*((vect[k*4+1]-vect[j*4+1])+(vect[k*4+3]-vect[j*4+3]))
            agent = np.append(agent, [-u1, -u2])
            output=self.phi_alpha(np.append(output, agent))
        return(output)

    def euler(self):
        """ Méthode d'Euler pour approcher le consensus
        entre les agents
        """
        t = self.pas
        output = np.array([self.init_matrice])
        while t<=self.temps:
            Z = self.pas*self.deriv(output[-1])
            #//Z = self.pas*self.phi_alpha(np.dot(self.mtransition,output[-1]))
            output = np.append(output, [output[-1]+Z], axis=0)
            t += self.pas
        #//print("X = ", output)
        return(output)
    
    def distance(self, status):
        """ Retourne les écarts de valeur entre les paramètres
        des agents.
    "   """
        output = np.array([])
        for k in range(len(self.agents)):
            pos_x = 0
            pos_y = 0
            vit_x = 0
            vit_y = 0
            for j in range(len(self.agents)):
                pos_x += self.madjacence[k][j]*(status[k*4]-status[j*4])
                pos_y += self.madjacence[k][j]*(status[k*4+1]-status[k*4+1])
                vit_x += self.madjacence[k][j]*(status[k*4+2]-status[k*4+2])
                vit_y += self.madjacence[k][j]*(status[k*4+3]-status[k*4+3])
            agent = np.array([pos_x, pos_y, vit_x, vit_y])
            output=np.append(output, agent)
        return(output)

    def lossFct(self):
        """ Calcule la fonction de coût pour chaque iterations
        menant au consensus
        """
        output = np.zeros(self.consensus.shape)
        for i in range(self.consensus.shape[0]):
            output[i] = self.distance(self.consensus[i])
        return(output)

    def show(self):
        """ Affiche le graphe représentant le système
        """
        repr = ['r*','b*','g*','m*','y*','c*']
        for k in range(len(self.agents)):
            axis_x_agent = [state[k*4] for state in self.consensus]
            axis_y_agent = [state[k*4+1] for state in self.consensus]
            plt.plot(axis_x_agent, axis_y_agent, repr[k] if k<6 else 'k*')
        plt.show()


####################################
############| PROGRAM |#############
####################################

if __name__=="__main__" :
    # Environnement de test (provisoire)
    agents = [Agent(4) for i in range(6)]
    A = np.array([[0, 1, 1, 1, 1, 1],
                  [1, 0, 1, 1, 1, 1],
                  [1, 1, 0, 1, 1, 1],
                  [1, 1, 1, 0, 1, 1],
                  [1, 1, 1, 1, 0, 1],
                  [1, 1, 1, 1, 1, 0]
                ])
    sys = System(agents, pas=1, temps=5, madjacence=A)
    #//print(sys.consensus)
    #//sys.show()