import os
import glob


def get_file_metadata(filename):
    first_split = os.path.split(filename)
    category = os.path.split(first_split[0])[1]
    context = {"category": category}
    return filename, context


def get_files(datadir):
    files = glob.glob(os.path.join(datadir, "*/*.txt"))
    w_metadata = [get_file_metadata(f) for f in files]
    return w_metadata


def get_texts(files):
    for descriptor in files:
        filename, context = descriptor
        with open(filename, "r") as f:
            text = f.read()

        yield (text, context)
