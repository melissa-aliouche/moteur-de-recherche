# -*- coding: utf-8 -*-

class Author:
    
    def __init__(self, name):
        self.name = name          
        self.ndoc = 0             # Nombre de documents publiés
        self.production = {}      # Dictionnaire des documents (id -> objet Document)
    
    def __str__(self):
        return self.name          # Affiche uniquement le nom
    
    def add(self, cle, document):
        # Ajoute un document à la production et incrémente le compteur
        self.production[cle] = document
        self.ndoc += 1
        
    def tailleMoy(self): # Calcule la taille moyenne des textes de l’auteur
        if len(self.production) == 0:
            return 0
        s = 0
        for e in self.production.values():
            s += len(e.texte)
        return s / len(self.production)
