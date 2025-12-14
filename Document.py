# -*- coding: utf-8 -*-

from datetime import datetime

class Document:
    
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
    
    def __str__(self):
        return self.titre
    
    def afficher(self): # Affiche toutes les infos principales du document
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Texte: {self.texte[:100]}...")
    
    def getType(self): # Type générique
        return "Document"


class RedditDocument(Document):
    
    def __init__(self, titre, auteur, date, url, texte, num_comments):
        super().__init__(titre, auteur, date, url, texte)
        self.num_comments = num_comments
    
    def __str__(self):
        return f"[Reddit] {self.titre}"
    
    def get_num_comments(self):
        return self.num_comments
    
    def set_num_comments(self, num_comments):
        self.num_comments = num_comments
    
    def getType(self):
        return "Reddit"
    
    def afficher(self):
        super().afficher()
        print(f"Nombre de commentaires: {self.num_comments}")


class ArxivDocument(Document):
    
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
    
    def __str__(self):
        return f"[Arxiv] {self.titre}"
    
    def get_co_auteurs(self):
        return self.co_auteurs
    
    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs
    
    def getType(self):
        return "Arxiv"
    
    def afficher(self):
        super().afficher()
        print(f"Co-auteurs: {', '.join(self.co_auteurs)}")