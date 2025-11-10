# -*- coding: utf-8 -*-

import praw
import urllib.request
import xmltodict
import pandas as pd
from datetime import datetime
from Corpus import Corpus
from DocumentFactory import DocumentFactory

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
