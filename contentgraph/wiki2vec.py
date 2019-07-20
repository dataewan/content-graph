from . import config
from wikipedia2vec import Wikipedia2Vec
from itertools import groupby
import csv


class WikiInterface(object):

    """Connects to the wiki2vec API to give access"""

    def __init__(self, entity_filename=config.out_ent_filename):
        self.wiki2vec = Wikipedia2Vec.load(config.wiki_model_file)
        self.entity_filename = entity_filename

    def get_entity_vector(self, entity):
        try:
            return self.wiki2vec.get_entity_vector(entity)

        except KeyError as e:
            return None

    @staticmethod
    def entity_file_keyfunc(row):
        return row["filename"]

    @staticmethod
    def row_get_entity_keyfunc(row):
        return row["entity"]

    @staticmethod
    def aggregate_article_and_entity_vectors(article_vector, entity_vector):
        if entity_vector is not None:
            if article_vector is None:
                return entity_vector
            return article_vector + entity_vector
        return None

    def get_article_vector(self, entities):
        article_vector = None

        for row in entities:
            entity = self.row_get_entity_keyfunc(row)
            entity_vector = self.get_entity_vector(entity)
            article_vector = self.aggregate_article_and_entity_vectors(
                article_vector, entity_vector
            )

        return article_vector

    @staticmethod
    def process_text(filename):
        with open(filename, "r") as f:
            headline = f.readline().strip()
            text = f.readlines()

        return headline, text

    def get_article_embeddings(self):
        self.article_vectors = []
        idx = 0
        with open(self.entity_filename, "r") as f:
            reader = csv.DictReader(f)
            for filename, entities in groupby(reader, self.entity_file_keyfunc):
                article_vector = self.get_article_vector(entities)
                headline, text = self.process_text(filename)
                self.article_vectors.append(
                    {
                        "idx": str(idx),
                        "filename": filename,
                        "article_vector": article_vector,
                        "headline": headline,
                        "text": text,
                    }
                )
                idx += 1
