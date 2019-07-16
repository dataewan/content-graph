import os
import glob
import csv
from .config import out_ent_filename

import logging

logging.basicConfig(level=logging.DEBUG)


def get_file_metadata(filename):
    first_split = os.path.split(filename)
    category = os.path.split(first_split[0])[1]
    context = {"category": category, "filename": filename}
    return filename, context


def get_files(datadir):
    files = glob.glob(os.path.join(datadir, "*/*.txt"))
    w_metadata = [get_file_metadata(f) for f in files]
    return w_metadata


def get_texts(files):
    for descriptor in files:
        filename, context = descriptor
        logging.debug("reading {}".format(filename))
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        yield (text, context)


def output_ents(ents):
    with open(out_ent_filename, "w") as f:
        writer = csv.writer(f)

        writer.writerow(["entity", "type", "category", "filename"])

        for entity in ents:
            writer.writerows(entity)
