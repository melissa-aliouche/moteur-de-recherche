# Moteur de Recherche Python

Un moteur de recherche complet pour récupérer, structurer, analyser et rechercher des documents provenant de Reddit et Arxiv

- **Rapport (PDF)** : [Rapport_Projet_Python.pdf](./Projet_Python_Melissa_Aliouche-Zehua_Zheng.pdf)

## À propos

Ce projet implémente un moteur de recherche capable de récupérer et d'analyser des documents provenant de deux sources principales :
- Reddit (via l'API PRAW)
- Arxiv (via urllib et xmltodict)

Le projet met en œuvre des concepts avancés de programmation orientée objet, des patrons de conception (Singleton, Factory), des techniques d'analyse textuelle et un moteur de recherche basé sur TF-IDF.

Le projet a ensuite été étendu (TD8–TD10) avec une interface Jupyter interactive (ipywidgets) et des analyses avancées (filtres, évolution temporelle et OKAPI‑BM25).

## Fonctionnalités

- Récupération automatique de documents depuis Reddit et Arxiv
- Analyse statistique des documents (nombre de mots, phrases, etc.)
- Gestion des auteurs et de leurs productions
- Sauvegarde et chargement du corpus en format TSV
- Architecture orientée objet avec patrons de conception
- Polymorphisme et héritage pour gérer différents types de documents
- Recherche par mots-clés avec expressions régulières
- Concordancier pour analyser le contexte des termes
- Nettoyage et normalisation des textes
- Calcul de statistiques textuelles (vocabulaire, fréquences TF/DF)
- Moteur de recherche avec matrices TF et TF-IDF
- Recherche par similarité cosinus
- Interface graphique sous Jupyter Notebook
- Comparaison de sous-corpus (par auteur / type)
- Évolution temporelle des mots
- Analyse du vocabulaire avec scores TF-IDF et OKAPI-BM25

## Structure du projet
```
.
├── Author.py                # Gestion des auteurs et leurs documents
├── Document.py              # Classes Document, RedditDocument, ArxivDocument
├── Corpus.py                # Singleton pour gérer l'ensemble des documents
├── DocumentFactory.py       # Factory pour créer les documents par type
├── SearchEngine.py          # Moteur de recherche avec TF-IDF
├── main.py                  # Programme principal
└── Interface_Jupyter.ipynb  # Notebook TD8–TD10 (widgets + analyses)
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

Installez les bibliothèques nécessaires :
```bash
pip install praw pandas xmltodict scipy numpy
```

### Configuration Reddit

Créez une application Reddit sur reddit.com/prefs/apps et configurez vos identifiants dans main.py :
```python
reddit = praw.Reddit(
    client_id="VOTRE_CLIENT_ID",
    client_secret="VOTRE_CLIENT_SECRET",
    user_agent="VOTRE_USER_AGENT"
)
```

## Utilisation

### Lancement du programme
```bash
python main.py
```

### Notebook (TD7–TD10)

```bash

jupyter notebook

# ouvrir Interface_Jupyter.ipynb

```

> Le notebook utilise un fichier `corpus.tsv` (créé par `main.py` s'il n'existe pas).

### Exemple de workflow

1. Le programme récupère des documents sur un thème (ex: "machine learning")
2. Les documents sont nettoyés et structurés
3. Le corpus est sauvegardé dans corpus.tsv
4. Des statistiques sont affichées pour chaque auteur
5. Les documents sont listés et triés
6. Le moteur de recherche est initialisé
7. Recherche interactive par mots-clés

### Utilisation des classes

#### Corpus
```python
from Corpus import Corpus
from DocumentFactory import DocumentFactory

# Récupérer l'instance unique du corpus
corpus = Corpus("MonCorpus")

# Créer un document via la factory
doc = DocumentFactory.create_document(
    doc_type="reddit",
    titre="Titre du post",
    auteur="username",
    date="2025-01-15",
    url="https://...",
    texte="Contenu du post",
    num_comments=42
)

# Ajouter au corpus
corpus.add(doc)

# Afficher les statistiques
corpus.show(tri="date")

# Recherche de passages
passages = corpus.search("machine learning")

# Créer un concordancier
concordancier = corpus.concorde("neural", taille_contexte=50)

# Statistiques textuelles
corpus.stats(n=20)
```

#### Moteur de recherche
```python
from SearchEngine import SearchEngine

# Créer le moteur de recherche
moteur = SearchEngine(corpus)

# Effectuer une recherche
resultats = moteur.search("deep learning neural network", nb_resultats=10)

# Afficher les résultats
print(resultats[['titre', 'auteur', 'score']])
```

## Architecture

### Patrons de conception implémentés

#### Singleton (Corpus)
Garantit qu'une seule instance du corpus existe, évitant les duplications de données.
```python
corpus = Corpus("MonCorpus")
```

#### Factory (DocumentFactory)
Crée automatiquement le bon type de document selon la source.
```python
doc = DocumentFactory.create_document(doc_type="reddit", ...)
```

### Hiérarchie des classes
```
Document (classe parente)
├── RedditDocument (+ num_comments)
└── ArxivDocument (+ co_auteurs)
```

## Fonctionnalités détaillées

### Classe Author
- add(doc) : Ajoute un document à la production de l'auteur
- tailleMoy() : Calcule la taille moyenne des documents

### Classe Document
- afficher() : Affiche les métadonnées et un extrait
- getType() : Retourne le type de document

### Classe Corpus
- add(doc) : Ajoute un document au corpus
- show(tri) : Affiche les documents (tri par date ou titre)
- save(fichier) : Sauvegarde le corpus en TSV
- load(fichier) : Charge un corpus depuis un fichier
- search(mot_clef) : Recherche des passages contenant un mot-clé
- concorde(expression, taille_contexte) : Crée un concordancier
- nettoyer_texte(texte, remove_stopwords) : Nettoie et normalise un texte
- stats(n) : Affiche les statistiques textuelles du corpus
- set_stopwords(enabled) : Active/désactive la suppression des stopwords

### Classe SearchEngine
- search(mots_clefs, nb_resultats) : Recherche les documents pertinents
- afficher_stats_vocab() : Affiche les statistiques du vocabulaire

## Statistiques disponibles

- Nombre total de documents
- Répartition par source (Reddit/Arxiv)
- Nombre de mots et phrases par document
- Statistiques par auteur (nombre de docs, taille moyenne)
- Longueur totale du texte combiné
- Vocabulaire complet du corpus
- Fréquences des termes (TF)
- Fréquences documentaires (DF)
- Mots les plus fréquents

## Algorithmes implémentés

### TF (Term Frequency)
Compte le nombre d'occurrences de chaque terme dans chaque document.

### TF-IDF (Term Frequency - Inverse Document Frequency)
Pondère l'importance d'un terme en fonction de sa rareté dans le corpus :

$$
\mathrm{TF\text{-}IDF} = \mathrm{TF}\cdot \log\left(\frac{N}{\mathrm{DF}}\right)
$$

où $N$ est le nombre total de documents et $\mathrm{DF}$ le nombre de documents contenant le terme.

### Similarité Cosinus
Mesure la similarité entre la requête et les documents :

$$
\mathrm{similarité}=\frac{A\cdot B}{\lVert A\rVert\,\lVert B\rVert}
$$

### OKAPI-BM25
Mesure plus robuste que TF-IDF lorsque les documents ont des longueurs différentes :

$$
\mathrm{score}(D,Q)=\sum_{t\in Q} IDF(t)\cdot
\frac{f(t,D)\,(k_1+1)}{f(t,D)+k_1\left(1-b+b\cdot\frac{|D|}{avgdl}\right)}
$$

## Contexte pédagogique

Ce projet a été développé dans le cadre des TD3, TD4, TD5, TD6 et TD7 :

| TD | Objectif | Concepts |
|----|----------|----------|
| TD3 | Acquisition de données | APIs, Pandas, nettoyage de texte |
| TD4 | Structuration OOP | Classes, encapsulation, modules |
| TD5 | Patrons avancés | Héritage, Singleton, Factory |
| TD6 | Analyse textuelle | Expressions régulières, concordancier, statistiques TF/DF |
| TD7 | Moteur de recherche | Matrices TF-IDF, similarité cosinus, recherche vectorielle |
| TD8 | Interface Notebook | Jupyter, ipywidgets, tqdm, découpage en phrases |
| TD9–TD10 | Projet libre | Filtres, comparaison de corpus, évolution temporelle, TF-IDF & BM25 |

## Technologies utilisées

- Python 3.8+
- PRAW (Reddit API)
- Pandas (manipulation de données)
- NumPy (calcul numérique)
- SciPy (matrices sparse)
- xmltodict (parsing XML pour Arxiv)
- re (expressions régulières)
- Jupyter Notebook (interface interactive)
- ipywidgets (widgets UI)
- tqdm (barres de progression)
- Matplotlib (visualisations)

## Améliorations possibles

- Ajouter des stop-words pour filtrer les mots communs
- Implémenter la lemmatisation
- Ajouter d'autres sources de données
- Créer une interface graphique
- Implémenter le PageRank pour le classement
- Ajouter la recherche floue
- Optimiser les performances pour de gros corpus

## Auteur

- Mélissa Aliouche  
- Zehua Zheng  

Année universitaire 2025–2026
