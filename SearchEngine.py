# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 21:21:33 2025

@author: maliouche
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import math

class SearchEngine:
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = {}
        self.mat_TF = None
        self.mat_TFxIDF = None
        
        # construction automatique lors de l'instanciation
        self._construire_vocabulaire()
        self._construire_matrices()
    
    def _construire_vocabulaire(self):
        # récupérer les mots uniques et les trier
        mots_uniques = set()
        
        for doc in self.corpus.id2doc.values():
            texte_nettoye = self.corpus.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            mots_uniques.update([mot for mot in mots if mot])
        
        # créer le dictionnaire vocab avec identifiants
        mots_tries = sorted(list(mots_uniques))
        for idx, mot in enumerate(mots_tries):
            self.vocab[mot] = {
                'id': idx,
                'total_occurrences': 0,
                'nb_documents': 0
            }
    
    def _construire_matrices(self):
        nb_docs = len(self.corpus.id2doc)
        nb_mots = len(self.vocab)
        
        # matrice TF en format sparse
        row_indices = []
        col_indices = []
        data_tf = []
        
        # Dictionnaire pour compter les occurrences par document
        doc_freq = {mot: 0 for mot in self.vocab}
        
        # pour chaque document
        for doc_id, doc in self.corpus.id2doc.items():
            texte_nettoye = self.corpus.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            
            # Compter les occurrences de chaque mot dans le document
            mot_counts = {}
            mots_vus = set()
            
            for mot in mots:
                if mot and mot in self.vocab:
                    mot_counts[mot] = mot_counts.get(mot, 0) + 1
                    mots_vus.add(mot)
            
            # Remplir la matrice 
            for mot, count in mot_counts.items():
                row_indices.append(doc_id)
                col_indices.append(self.vocab[mot]['id'])
                data_tf.append(count)
                self.vocab[mot]['total_occurrences'] += count
            
            for mot in mots_vus:
                doc_freq[mot] += 1
        
        # Mettre à jour le nombre de documents pour chaque mot
        for mot in self.vocab:
            self.vocab[mot]['nb_documents'] = doc_freq[mot]
        
        self.mat_TF = csr_matrix((data_tf, (row_indices, col_indices)), 
                                  shape=(nb_docs, nb_mots))
        
        # Calculer la matrice TFxIDF
        self._calculer_TFxIDF()
    
    def _calculer_TFxIDF(self):
        nb_docs = len(self.corpus.id2doc)
        
        # Calculer IDF pour chaque mot
        idf = np.zeros(len(self.vocab))
        for mot, info in self.vocab.items():
            mot_id = info['id']
            nb_docs_avec_mot = info['nb_documents']
            if nb_docs_avec_mot > 0:
                idf[mot_id] = math.log(nb_docs / nb_docs_avec_mot)
            else:
                idf[mot_id] = 0
        
        # Multiplier TF par IDF 
        self.mat_TFxIDF = self.mat_TF.multiply(idf)
    
    def _vectoriser_requete(self, mots_clefs):
        # créer un vecteur pour la requête
        vecteur = np.zeros(len(self.vocab))
        
        mots_clefs_nettoyes = self.corpus.nettoyer_texte(mots_clefs).split()
        
        for mot in mots_clefs_nettoyes:
            if mot in self.vocab:
                mot_id = self.vocab[mot]['id']
                vecteur[mot_id] += 1
        
        return vecteur
    
    def _similarite_cosinus(self, vecteur_requete, matrice_docs):
        # calculer le produit scalaire entre la requête et tous les documents
        scores = matrice_docs.dot(vecteur_requete)
        
        # ccalculer les normes
        norme_requete = np.linalg.norm(vecteur_requete)
        normes_docs = np.sqrt(matrice_docs.multiply(matrice_docs).sum(axis=1).A1)
        
        # Éviter la division par zéro
        normes_docs[normes_docs == 0] = 1
        
        if norme_requete == 0:
            return np.zeros(len(scores))
        
        # calculer la similarité cosinus
        similarites = scores / (normes_docs * norme_requete)
        
        return similarites
    
    def search(self, mots_clefs, nb_resultats=10):
        # Vectoriser la req
        vecteur_requete = self._vectoriser_requete(mots_clefs)
        
        # la similarité cosinus avec TFxIDF
        scores = self._similarite_cosinus(vecteur_requete, self.mat_TFxIDF)
        
        # Trier les docs par score décroissant
        indices_tries = np.argsort(scores)[::-1][:nb_resultats]
        
        # Créer le DataFrame de résultats
        resultats = []
        for idx in indices_tries:
            if scores[idx] > 0:
                doc = self.corpus.id2doc[idx]
                resultats.append({
                    'doc_id': idx,
                    'titre': doc.titre,
                    'auteur': doc.auteur,
                    'date': doc.date,
                    'url': doc.url,
                    'score': scores[idx],
                    'type': doc.getType()
                })
        
        return pd.DataFrame(resultats)
    
    def afficher_stats_vocab(self):
        print(f"Taille du vocabulaire : {len(self.vocab)} mots")
        print(f"\nExemple de mots dans le vocabulaire :")
        for i, (mot, info) in enumerate(list(self.vocab.items())[:10]):
            print(f"  - {mot} : {info['total_occurrences']} occurrences, "
                  f"{info['nb_documents']} documents")