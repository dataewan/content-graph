from contentgraph import data, textproc
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)

DATADIR = "/home/ewan/data/bbc-datasets/bbc-news/bbc/"


def extract():
    files = data.get_files(DATADIR)
    texts = data.get_texts(files)
    logging.debug("Setting up NLP")
    
    nlp = textproc.setup_nlp()
    docs = textproc.create_docs(nlp, texts)
    ents = textproc.process_docs(nlp, docs)
    data.output_ents(ents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true")


    args = parser.parse_args()

    if args.extract:
        extract()
