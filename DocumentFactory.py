# -*- coding: utf-8 -*-

from Document import Document, RedditDocument, ArxivDocument

class DocumentFactory:
    
    @staticmethod
    def create_document(doc_type, titre, auteur, date, url, texte, **kwargs):
        if doc_type == "reddit":
            num_comments = kwargs.get('num_comments', 0)
            return RedditDocument(titre, auteur, date, url, texte, num_comments)
        elif doc_type == "arxiv":
            co_auteurs = kwargs.get('co_auteurs', [])
            return ArxivDocument(titre, auteur, date, url, texte, co_auteurs)
        else:
            return Document(titre, auteur, date, url, texte)