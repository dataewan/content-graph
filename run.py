from contentgraph import data, textproc, graph_tools
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



def do_graph():
    G = graph_tools.create_graph()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true", help="Run NLP extract")


    args = parser.parse_args()

    if args.extract:
        do_extract()
