from contentgraph import data, textproc

DATADIR = "/home/ewan/data/bbc-datasets/bbc-news/bbc/"

if __name__ == "__main__":
    files = data.get_files(DATADIR)
    # testing subset, should be removed later
    files = files[:4]
    texts = data.get_texts(files)
    nlp = textproc.setup_nlp()
    docs = textproc.process_texts(nlp, texts)
