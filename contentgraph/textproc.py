import spacy
from spacy.tokens import Doc


def setup_nlp():
    Doc.set_extension("filename", default=None)
    Doc.set_extension("category", default=None)
    nlp = spacy.load("en_core_web_md")
    return nlp


def process_texts(nlp, texts):

    for doc, context in nlp.pipe(texts, as_tuples=True):
        doc._.category = context["category"]

        yield doc
