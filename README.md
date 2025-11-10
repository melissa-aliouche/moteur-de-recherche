# 🔍 Moteur de Recherche Python

> Un moteur de recherche pour récupérer, structurer et analyser des documents provenant de Reddit et Arxiv

## 📋 À propos

Ce projet implémente un moteur de recherche capable de récupérer et d'analyser des documents provenant de deux sources principales :
- **Reddit** (via l'API PRAW)
- **Arxiv** (via urllib et xmltodict)

Le projet met en œuvre des concepts avancés de programmation orientée objet et des patrons de conception (Singleton, Factory) pour garantir une architecture propre et extensible.

## ✨ Fonctionnalités

- 🔎 Récupération automatique de documents depuis Reddit et Arxiv
- 📊 Analyse statistique des documents (nombre de mots, phrases, etc.)
- 👥 Gestion des auteurs et de leurs productions
- 💾 Sauvegarde et chargement du corpus en format TSV
- 🏗️ Architecture orientée objet avec patrons de conception
- 🔄 Polymorphisme et héritage pour gérer différents types de documents

## 🗂️ Structure du projet

```
.
├── Author.py           # Gestion des auteurs et leurs documents
├── Document.py         # Classes Document, RedditDocument, ArxivDocument
├── Corpus.py           # Singleton pour gérer l'ensemble des documents
├── DocumentFactory.py  # Factory pour créer les documents par type
└── main.py             # Programme principal
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

Installez les bibliothèques nécessaires :

```bash
pip install praw pandas xmltodict
```

### Configuration Reddit

Créez une application Reddit sur [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) et configurez vos identifiants dans `main.py` :

```python
reddit = praw.Reddit(
    client_id="VOTRE_CLIENT_ID",
    client_secret="VOTRE_CLIENT_SECRET",
    user_agent="VOTRE_USER_AGENT"
)
```

## 💻 Utilisation

### Lancement du programme

```bash
python main.py
```

### Exemple de workflow

1. Le programme récupère des documents sur un thème (ex: "machine learning")
2. Les documents sont nettoyés et structurés
3. Le corpus est sauvegardé dans `corpus.tsv`
4. Des statistiques sont affichées pour chaque auteur
5. Les documents sont listés et triés

### Utilisation des classes

```python
from Corpus import Corpus
from DocumentFactory import DocumentFactory

# Récupérer l'instance unique du corpus
corpus = Corpus.getInstance("MonCorpus")

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
```

## 🏗️ Architecture

### Patrons de conception implémentés

#### Singleton (Corpus)
Garantit qu'une seule instance du corpus existe, évitant les duplications de données.

```python
corpus = Corpus.getInstance("MonCorpus")
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

## 📊 Fonctionnalités détaillées

### Classe Author
- `add(doc)` : Ajoute un document à la production de l'auteur
- `tailleMoy()` : Calcule la taille moyenne des documents

### Classe Document
- `afficher()` : Affiche les métadonnées et un extrait
- `getType()` : Retourne le type de document

### Classe Corpus
- `add(doc)` : Ajoute un document au corpus
- `show(tri)` : Affiche les documents (tri par date ou titre)
- `save(fichier)` : Sauvegarde le corpus en TSV
- `load(fichier)` : Charge un corpus depuis un fichier

## 📈 Statistiques disponibles

- Nombre total de documents
- Répartition par source (Reddit/Arxiv)
- Nombre de mots et phrases par document
- Statistiques par auteur (nombre de docs, taille moyenne)
- Longueur totale du texte combiné

## 🎓 Contexte pédagogique

Ce projet a été développé dans le cadre des TD3, TD4 et TD5 :

| TD | Objectif | Concepts |
|----|----------|----------|
| **TD3** | Acquisition de données | APIs, Pandas, nettoyage de texte |
| **TD4** | Structuration OOP | Classes, encapsulation, modules |
| **TD5** | Patrons avancés | Héritage, Singleton, Factory |


## 👤 Auteur

**Mélissa Aliouche**  
Année universitaire 2025-2026
