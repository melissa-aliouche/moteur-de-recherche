# -*- coding: utf-8 -*-

from Document import Document
from Author import Author
import pandas as pd

class Corpus:
    _instance = None  # Singleton
    
    def __new__(cls, nom):
        #  Assure qu'une seule instance existe
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
            cls._instance.nom = nom
            cls._instance.authors = {}
            cls._instance.id2doc = {}
            cls._instance.ndoc = 0
            cls._instance.naut = 0
        return cls._instance
    
    def __init__(self, nom):
        pass
        
    def add(self, doc):
        cle = self.ndoc
        self.id2doc[cle] = doc
        self.ndoc += 1
        
        auteur_nom = doc.auteur
        if auteur_nom not in self.authors:
            self.authors[auteur_nom] = Author(auteur_nom)
            self.naut += 1
        
        self.authors[auteur_nom].add(cle, doc)
        
        return cle
    
    def show(self, n_docs=-1, tri=""):
        docs_list = list(self.id2doc.values())
        
        if tri == "date":
            docs_list.sort(key=lambda x: x.date)
        elif tri == "titre":
            docs_list.sort(key=lambda x: x.titre)
        
        if n_docs == -1:
            n_docs = len(docs_list)
        
        for i, doc in enumerate(docs_list[:n_docs]):
            print(f"{i+1}. [{doc.getType()}] {doc.titre} - {doc.auteur} ({doc.date})")
    
    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} documents, {self.naut} auteurs"
    
    def to_dataframe(self):
        data = []
        for doc_id, doc in self.id2doc.items():
            row = {
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.getType()
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def save(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename, sep="\t", index=False)
    
    @staticmethod
    def load(filename):
        df = pd.read_csv(filename, sep="\t")
        return df
