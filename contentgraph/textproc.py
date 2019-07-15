import spacy
from spacy.tokens import Doc
import logging

logging.basicConfig(level=logging.DEBUG)

ENT_TYPE_IGNORES = [
    "CARDINAL",
    "DATE",
    "MONEY",
    "ORDINAL",
    "PERCENT",
    "QUANTITY",
    "TIME",
]


def setup_nlp():
    Doc.set_extension("filename", default=None, force=True)
    Doc.set_extension("category", default=None, force=True)
    nlp = spacy.load("en_core_web_md")
    return nlp


def create_docs(nlp, texts):

    for doc, context in nlp.pipe(texts, as_tuples=True):
        doc._.category = context["category"]
        doc._.filename = context["filename"]

        yield doc


def entity_to_item(ent, doc):
    return (ent.lower_, ent.label_, doc._.category, doc._.filename)


def get_entities(doc):
    return list(
        set(
            [
                entity_to_item(ent, doc)
                for ent in doc.ents
                if ent.label_ not in ENT_TYPE_IGNORES
            ]
        )
    )


def process_docs(nlp, docs):
    for doc in docs:
        logging.debug("Getting entities from {}".format(doc._.filename))
        ents = get_entities(doc)

        yield ents
