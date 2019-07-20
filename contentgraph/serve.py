from flask import Flask, request, jsonify, abort, render_template
from .config import article_embeddings_file
import pickle
import annoy
import random


app = Flask(__name__, template_folder="..")


def load_embeddings():
    with open(article_embeddings_file, "rb") as f:
        embeddings = pickle.load(f)
    return embeddings


def get_idx(embedding):
    return embedding.get("idx")


def get_vector(embedding):
    return embedding.get("article_vector")


def get_headline(embedding):
    return embedding.get("headline")


def get_text(embedding):
    return embedding.get("text")


def process_embeddings(embeddings):
    lookup = {}
    for embedding in embeddings:
        idx = get_idx(embedding)
        vector = get_vector(embedding)
        headline = get_headline(embedding)
        text = get_text(embedding)
        if vector is not None:
            lookup[idx] = {
                "idx": idx,
                "vector": vector,
                "headline": headline,
                "text": text,
            }

    return lookup


def create_annoy_index(lookup, n_trees=30):
    embedding = lookup[list(lookup.keys())[0]]
    a = annoy.AnnoyIndex(len(embedding["vector"]))

    for embedding in lookup.values():
        vec = embedding["vector"]
        idx = int(embedding["idx"])
        a.add_item(idx, vec)

    a.build(n_trees)
    return a


def prepare():
    embeddings = load_embeddings()
    lookup = process_embeddings(embeddings)
    annoy_index = create_annoy_index(lookup)
    return lookup, annoy_index


lookup, annoy_index = prepare()


def find_ids_in_lookup():
    ids = list(lookup.keys())
    return ids


@app.route("/ids", methods=["GET"])
def get_ids():
    return jsonify(find_ids_in_lookup())


def get_neighbours(idx, N=5):
    idx = int(idx)
    neighbours = annoy_index.get_nns_by_item(idx, N)
    return [
        {"neighbour_idx": n_idx, "neighbour_headline": lookup[str(n_idx)]["headline"]}
        for n_idx in neighbours
    ]


def process_article(idx):
    article = lookup[idx]
    return {
        "headline": article.get("headline"),
        "text": article.get("text"),
        "neighbours": get_neighbours(idx),
    }


def deal_with_id(idx):
    if idx is None:
        return process_article(random.choice(find_ids_in_lookup()))
    if idx in lookup:
        return process_article(idx)
    return None


@app.route("/article", methods=["GET"])
def predict():
    idx = request.args.get("id")
    response = deal_with_id(idx)
    if response is not None:
        return jsonify(response)
    else:
        abort(404)


@app.route("/")
def interface():
    idx = request.args.get("id")
    article = deal_with_id(idx)
    if article is not None:
        return render_template("index.html", article=article)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
