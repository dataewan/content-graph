from contentgraph import data, textproc, wiki2vec
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)

DATADIR = "/home/ewan/data/bbc-datasets/bbc-news/bbc/"


def do_extract():
    files = data.get_files(DATADIR)
    texts = data.get_texts(files)
    logging.debug("Setting up NLP")
    
    nlp = textproc.setup_nlp()
    docs = textproc.create_docs(nlp, texts)
    ents = textproc.process_docs(nlp, docs)
    data.output_ents(ents)



def do_vectorise():
    wi = wiki2vec.WikiInterface()
    wi.get_article_embeddings()
    data.output_article_vectors(wi.article_vectors)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true", help="Run NLP extract")
    parser.add_argument("--vectorise", action="store_true", help="Run wiki2vec")


    args = parser.parse_args()

    if args.extract:
        do_extract()

    if args.vectorise:
        do_vectorise()
