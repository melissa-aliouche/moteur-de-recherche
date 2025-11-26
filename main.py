# -*- coding: utf-8 -*-

import praw
import urllib.request
import xmltodict
import pandas as pd
from datetime import datetime
from Corpus import Corpus
from DocumentFactory import DocumentFactory
from SearchEngine import SearchEngine

THEME = "machine learning"
NB_DOCS_ARXIV = 5
NB_DOCS_REDDIT = 5

#création du corpus (Singleton)
corpus = Corpus("Mon Corpus ML")

print("Récupérer des données depuis Reddit")
reddit = praw.Reddit(
    client_id='G26th_edvZT5GcdyivWzcw',
    client_secret='wh_cBVDMSUlCX0uJCVlt_Qjn4Cd-mA',
    user_agent='monApp'
)
subreddit = reddit.subreddit("all")

for post in subreddit.search(THEME, limit=NB_DOCS_REDDIT):
    titre = post.title
    auteur = str(post.author)
    date = datetime.fromtimestamp(post.created_utc)
    url = f"https://reddit.com{post.permalink}"
    texte = (post.title + " " + post.selftext).replace("\n", " ")
    num_comments = post.num_comments
    # filtrer des textes trop courts (< 20 caractères)
    if len(texte.strip()) >= 20:
        doc = DocumentFactory.create_document(
            "reddit", titre, auteur, date, url, texte,
            num_comments=num_comments
        )
        corpus.add(doc)

print(f"Reddit : {corpus.ndoc} documents récupérés")

print("Récupérer des données depuis Arxiv")
base_url = "http://export.arxiv.org/api/query?"
query = f"search_query=all:{THEME.replace(' ', '+')}&start=0&max_results={NB_DOCS_ARXIV}"
url = base_url + query

with urllib.request.urlopen(url) as response:
    data = response.read()

parsed = xmltodict.parse(data)
entries = parsed["feed"].get("entry", [])

if isinstance(entries, dict):
    entries = [entries]

for entry in entries:
    titre = entry.get("title", "").replace("\n", " ")

    authors_data = entry.get("author", [])
    if isinstance(authors_data, dict):
        authors_data = [authors_data]

    authors_list = [a.get("name", "Unknown") for a in authors_data]
    auteur = authors_list[0] if authors_list else "Unknown"
    co_auteurs = authors_list[1:] if len(authors_list) > 1 else []

    date_str = entry.get("published", "")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except:
        date = datetime.now()

    url = entry.get("id", "")
    texte = entry.get("summary", "").replace("\n", " ")

    # filtrer des textes trop courts
    if len(texte.strip()) >= 20:
        doc = DocumentFactory.create_document(
            "arxiv", titre, auteur, date, url, texte,
            co_auteurs=co_auteurs
        )
        corpus.add(doc)

print(f"Arxiv : {len(entries)} documents ajoutés")


# afficher le résumé du corpus
print(f"\n{corpus}")
# sauvegarde du corpus sur disque
corpus.save("corpus.tsv")
print("\nFichier 'corpus.tsv' sauvegardé avec succès.")
#Affichage des documents triés
print("\nAffichage des documents triés par date:")
corpus.show(n_docs=5, tri="date")

# statistiques de contenu 
print("\n--- Statistiques sur le contenu des documents ---")
for doc_id, doc in corpus.id2doc.items():
    nb_mots = len(doc.texte.split())
    nb_phrases = len([p for p in doc.texte.split('.') if p.strip()])
    print(f"[{doc.getType()}] {doc.titre} : {nb_mots} mots, {nb_phrases} phrases")

# création d'une chaîne unique de tous les textes
texte_total = " ".join([doc.texte for doc in corpus.id2doc.values()])
print(f"\nLongueur totale du texte combiné : {len(texte_total)} caractères")

# statistiques sur les auteurs 
print("\n--- Statistiques auteurs ---")
nom_auteur = input("Entrez le nom d'un auteur pour voir ses statistiques: ")
if nom_auteur in corpus.authors:
    auteur = corpus.authors[nom_auteur]
    print(f"Auteur: {auteur}")
    print(f"Nombre de documents: {auteur.ndoc}")
    print(f"Taille moyenne des documents: {auteur.tailleMoy():.2f} caractères")
else:
    print("Auteur non trouvé dans le corpus.")

# TD6

print("\n1. Test de la fonction search:")
mot_recherche = "learning"
passages = corpus.search(mot_recherche)
print(f"Passages contenant '{mot_recherche}' : {len(passages)} trouvés")
for i, passage in enumerate(passages[:3]):
    print(f"  {i+1}. ...{passage}...")

print("\n2. Test de la fonction concorde:")
concordancier = corpus.concorde("machine", taille_contexte=40)
print(concordancier.head(10))

print("\n3. Statistiques textuelles complètes:")
freq_table = corpus.stats(n=15)

# TD7: moteur de recherche

moteur = SearchEngine(corpus)

# Afficher les statistiques du vocabulaire
print("\n--- Statistiques du vocabulaire ---")
moteur.afficher_stats_vocab()

# Test du moteur de recherche
print("\n--- Test du moteur de recherche ---")
requete = "deep learning neural network"
print(f"\nRecherche pour : '{requete}'")
resultats = moteur.search(requete, nb_resultats=5)

if len(resultats) > 0:
    print(f"\n{len(resultats)} résultats trouvés :")
    print(resultats[['titre', 'auteur', 'score', 'type']].to_string(index=False))
else:
    print("Aucun résultat trouvé.")

print("\n-------------moteur de recherche---------------")
while True:
    requete_user = input("\nEntrez votre requête (ou 'quit' pour quitter) : ")
    if requete_user.lower() == 'quit':
        break
    
    resultats = moteur.search(requete_user, nb_resultats=5)
    
    if len(resultats) > 0:
        print(f"\n{len(resultats)} résultats trouvés :")
        for idx, row in resultats.iterrows():
            print(f"\n{idx+1}. [{row['type']}] {row['titre']}")
            print(f"   Auteur: {row['auteur']}")
            print(f"   Score: {row['score']:.4f}")
            print(f"   URL: {row['url']}")
    else:
        print("Aucun résultat trouvé.")

print("\nLa recherche est terminée!")