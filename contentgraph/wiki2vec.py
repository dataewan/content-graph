from . import config
from wikipedia2vec import Wikipedia2Vec


class WikiInterface(object):

    """Connects to the wiki2vec API to give access"""

    def __init__(self):
        self.wiki2vec = Wikipedia2Vec.load(config.wiki_model_file)

    def get_entity_vector(self, entity):
        try:
            return self.wiki2vec.get_entity_vector(entity)
            
        except KeyError as e:
            return None
