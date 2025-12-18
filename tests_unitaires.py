
# -*- coding: utf-8 -*-
"""
Tests Unitaires pour le Moteur de Recherche
============================================
Ce fichier contient des tests simples pour valider les fonctionnalités 
principales du projet : Corpus et SearchEngine.

Pour exécuter les tests : python tests_unitaires.py
"""

from Corpus import Corpus
from SearchEngine import SearchEngine
import pandas as pd


def separateur(titre):
    """Affiche un séparateur visuel pour chaque test"""
    print("\n" + "=" * 60)
    print(f"TEST : {titre}")
    print("=" * 60)


# ============================================================
# Chargement du corpus (utilisé par tous les tests)
# ============================================================
print("Chargement du corpus depuis 'corpus.tsv'...")
corpus = Corpus.load("corpus.tsv", nom="Corpus Test")
print(f"Corpus chargé : {corpus}")


# ============================================================
# TEST 1.1 : Corpus.search(mot)
# But : Vérifier la recherche de passages contenant un mot-clé
# ============================================================
separateur("1.1 Corpus.search(mot)")

mot_test = "learning"
passages = corpus.search(mot_test)

print(f"Mot recherché : '{mot_test}'")
print(f"Nombre de passages trouvés : {len(passages)}")

# Afficher les 5 premiers passages
print(f"\nLes 5 premiers passages :")
for i, passage in enumerate(passages[:5]):
    print(f"  {i+1}. ...{passage}...")

# Vérification simple
assert len(passages) > 0, "Erreur : aucun passage trouvé pour 'learning'"
print("\n✓ Test réussi : des passages ont été trouvés")


# ============================================================
# TEST 1.2 : Corpus.concorde(expression, taille_contexte)
# But : Vérifier le concordancier KWIC (contexte gauche/droite)
# ============================================================
separateur("1.2 Corpus.concorde(expression, taille_contexte)")

expression_test = "machine"
taille_contexte = 40
concordancier = corpus.concorde(expression_test, taille_contexte)

print(f"Expression recherchée : '{expression_test}'")
print(f"Taille du contexte : {taille_contexte} caractères")
print(f"Nombre d'occurrences : {len(concordancier)}")

# Vérifier les colonnes du DataFrame
colonnes_attendues = ['contexte gauche', 'motif trouvé', 'contexte droit']
print(f"\nColonnes du DataFrame : {list(concordancier.columns)}")

# Afficher les 10 premières lignes
print(f"\nLes 10 premières occurrences :")
print(concordancier.head(10).to_string())

# Vérifications
assert isinstance(concordancier, pd.DataFrame), "Erreur : le résultat n'est pas un DataFrame"
assert list(concordancier.columns) == colonnes_attendues, "Erreur : colonnes incorrectes"
print("\n✓ Test réussi : concordancier correct avec les bonnes colonnes")


# ============================================================
# TEST 1.3 : Corpus.stats(n)
# But : Vérifier les statistiques de fréquence des mots
# ============================================================
separateur("1.3 Corpus.stats(n)")

n_mots = 15
print(f"Affichage des {n_mots} mots les plus fréquents :\n")
freq_table = corpus.stats(n=n_mots)

# Vérifier que le tableau contient les bonnes colonnes
colonnes_stats = ['mot', 'term_frequency', 'document_frequency']
assert list(freq_table.columns) == colonnes_stats, "Erreur : colonnes de stats incorrectes"

# Vérifier que term_frequency > 0 pour les mots retournés
assert freq_table['term_frequency'].iloc[0] > 0, "Erreur : fréquence invalide"

print("\n✓ Test réussi : statistiques calculées correctement")


# ============================================================
# TEST 1.4 : SearchEngine.search(requete, nb_resultats)
# But : Vérifier le moteur de recherche TF-IDF
# ============================================================
separateur("1.4 SearchEngine.search(requete, nb_resultats)")

# Créer le moteur de recherche
moteur = SearchEngine(corpus)

requete_test = "deep learning neural network"
nb_resultats = 5

print(f"Requête : '{requete_test}'")
print(f"Nombre de résultats demandés : {nb_resultats}")

resultats = moteur.search(requete_test, nb_resultats=nb_resultats)

print(f"\nRésultats trouvés : {len(resultats)}")

if len(resultats) > 0:
    # Afficher les résultats
    print("\nTableau des résultats :")
    print(resultats[['titre', 'auteur', 'type', 'score']].to_string())
    
    # Vérification 1 : les scores sont triés en ordre décroissant
    scores = resultats['score'].tolist()
    scores_tries = sorted(scores, reverse=True)
    assert scores == scores_tries, "Erreur : les scores ne sont pas triés"
    print("\n✓ Vérification : scores triés en ordre décroissant")
    
    # Vérification 2 : tous les scores sont > 0
    assert all(s > 0 for s in scores), "Erreur : certains scores sont <= 0"
    print("✓ Vérification : tous les scores sont positifs")
    
    # Vérification 3 : les colonnes essentielles sont présentes
    colonnes_requises = ['titre', 'auteur', 'type', 'score', 'url']
    for col in colonnes_requises:
        assert col in resultats.columns, f"Erreur : colonne '{col}' manquante"
    print("✓ Vérification : toutes les colonnes requises sont présentes")

print("\n✓ Test réussi : moteur de recherche fonctionne correctement")


# ============================================================
# TEST 1.5 : SearchEngine.afficher_stats_vocab()
# But : Vérifier l'affichage des statistiques du vocabulaire
# ============================================================
separateur("1.5 SearchEngine.afficher_stats_vocab()")

print("Statistiques du vocabulaire :\n")
moteur.afficher_stats_vocab()

# Vérifications
taille_vocab = len(moteur.vocab)
print(f"\nTaille du vocabulaire : {taille_vocab} mots")
assert taille_vocab > 0, "Erreur : vocabulaire vide"

print("\n✓ Test réussi : vocabulaire construit correctement")


# ============================================================
# TEST 1.6 : Test des stopwords (optionnel)
# But : Vérifier que la suppression des stopwords fonctionne
# ============================================================
separateur("1.6 Test des stopwords (optionnel)")

# Taille du vocabulaire sans stopwords
corpus.set_stopwords(False)
corpus._vocabulaire = None  # reset cache
corpus._freq = None
corpus.stats(n=5)
taille_sans_filtre = len(corpus._vocabulaire)
print(f"\nTaille vocabulaire SANS filtre stopwords : {taille_sans_filtre}")

# Taille du vocabulaire avec stopwords
corpus.set_stopwords(True)
corpus._vocabulaire = None  # reset cache
corpus._freq = None
corpus.stats(n=5)
taille_avec_filtre = len(corpus._vocabulaire)
print(f"\nTaille vocabulaire AVEC filtre stopwords : {taille_avec_filtre}")

# Vérification : le vocabulaire filtré doit être plus petit
assert taille_avec_filtre < taille_sans_filtre, "Erreur : stopwords non filtrés"
print(f"\nDifférence : {taille_sans_filtre - taille_avec_filtre} mots supprimés")

print("\n✓ Test réussi : filtrage des stopwords fonctionne")

# Remettre les stopwords désactivés par défaut
corpus.set_stopwords(False)


# ============================================================
# RÉSUMÉ DES TESTS
# ============================================================
print("\n" + "=" * 60)
print("RÉSUMÉ : TOUS LES TESTS ONT RÉUSSI ✓")
print("=" * 60)
print("""
Tests effectués :
  1.1 Corpus.search(mot)           - Recherche de passages
  1.2 Corpus.concorde()            - Concordancier KWIC
  1.3 Corpus.stats(n)              - Statistiques de fréquence
  1.4 SearchEngine.search()        - Moteur de recherche TF-IDF
  1.5 afficher_stats_vocab()       - Vocabulaire
  1.6 Stopwords                    - Filtrage des mots vides
""")