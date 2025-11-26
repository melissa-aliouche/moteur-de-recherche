# -*- coding: utf-8 -*-

from Document import Document
from Author import Author
import pandas as pd
import re

class Corpus:
    _instance = None # Variable de classe pour le singleton
    
    def __new__(cls, nom):
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
            cls._instance.nom = nom
            cls._instance.authors = {} # dictionnaire nom_auteur -> Author
            cls._instance.id2doc = {} # dictionnaire id_doc -> Document
            cls._instance.ndoc = 0
            cls._instance.naut = 0
            cls._instance._texte_total = None # cache du texte combiné de tout le corpus
            cls._instance._vocabulaire = None 
            cls._instance._freq = None
        return cls._instance
    
    def __init__(self, nom):
        pass # __init__ ne fait rien car tout est déjà initialisé dans __new__
        
    def add(self, doc): # Ajoute un document au corpus
        cle = self.ndoc
        self.id2doc[cle] = doc
        self.ndoc += 1
        # Ajouter l'auteur si il n'existe pas encore
        auteur_nom = doc.auteur
        if auteur_nom not in self.authors:
            self.authors[auteur_nom] = Author(auteur_nom)
            self.naut += 1
        
        self.authors[auteur_nom].add(cle, doc)
        
        # Réinitialiser les caches
        self._texte_total = None
        self._vocabulaire = None
        self._freq = None
        
        return cle
    
    def show(self, n_docs=-1, tri=""): # Affiche les documents du corpus, éventuellement triés par date ou titre
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
    
    def to_dataframe(self): # pour faciliter la manipulation
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
    
    def _construire_texte_total(self): # Concatène tous les textes des documents
        if self._texte_total is None:
            self._texte_total = " ".join([doc.texte for doc in self.id2doc.values()])
        return self._texte_total
    
    def search(self, mot_clef): # Recherche des passages contenant le mot-clé et renvoie les extraits
        texte_total = self._construire_texte_total()
        passages = re.findall(r'.{0,50}' + re.escape(mot_clef) + r'.{0,50}', texte_total, re.IGNORECASE)
        return passages
    
    def concorde(self, expression, taille_contexte=30):
        texte_total = self._construire_texte_total()
        
        pattern = r'(.{0,' + str(taille_contexte) + r'})(' + re.escape(expression) + r')(.{0,' + str(taille_contexte) + r'})'
        matches = re.finditer(pattern, texte_total, re.IGNORECASE)
        
        resultats = []
        for match in matches:
            contexte_gauche = match.group(1)
            motif_trouve = match.group(2)
            contexte_droit = match.group(3)
            resultats.append({
                'contexte gauche': contexte_gauche,
                'motif trouvé': motif_trouve,
                'contexte droit': contexte_droit
            })
        
        return pd.DataFrame(resultats)
    
    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = texte.replace('\n', ' ')
        texte = re.sub(r'[^\w\s]', ' ', texte)
        texte = re.sub(r'\d+', '', texte)
        texte = re.sub(r'\s+', ' ', texte)
        return texte.strip()
    
    def _construire_vocabulaire_et_freq(self):
        if self._vocabulaire is not None and self._freq is not None:
            return
        
        freq_dict = {}
        doc_freq_dict = {}
        vocabulaire = set()
        
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            
            mots_uniques_doc = set()
            
            for mot in mots:
                if mot:
                    vocabulaire.add(mot)
                    mots_uniques_doc.add(mot)
                    # fréquence totale dans le corpus
                    if mot in freq_dict:
                        freq_dict[mot] += 1
                    else:
                        freq_dict[mot] = 1
            # fréquence par document
            for mot in mots_uniques_doc:
                if mot in doc_freq_dict:
                    doc_freq_dict[mot] += 1
                else:
                    doc_freq_dict[mot] = 1
        
        self._vocabulaire = vocabulaire
        
        data = []
        for mot in vocabulaire:
            data.append({
                'mot': mot,
                'term_frequency': freq_dict.get(mot, 0),
                'document_frequency': doc_freq_dict.get(mot, 0)
            })
        
        self._freq = pd.DataFrame(data)
        self._freq = self._freq.sort_values(by='term_frequency', ascending=False).reset_index(drop=True)
    
    def stats(self, n=10):
        self._construire_vocabulaire_et_freq()
        
        print(f"Nombre de mots différents dans le corpus : {len(self._vocabulaire)}")
        print(f"\nLes {n} mots les plus fréquents :")
        print(self._freq.head(n).to_string(index=False))
        
        return self._freq