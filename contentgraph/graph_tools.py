import csv
from .config import out_ent_filename
import itertools
import networkx as nx


def node_getter(row):
    return (row["entity"], row["type"])

def get_edges(nodes):
    connections = itertools.combinations(nodes, 2)
    return list(connections)


def get_nodes(rows):
    return [node_getter(row) for row in rows]


def create_graph():
    G = nx.Graph()
    with open(out_ent_filename, "r") as f:
        reader = csv.DictReader(f)

        keyfunc = lambda x: x["filename"]

        for filename, rows in itertools.groupby(reader, keyfunc):
            rows = list(rows)
            nodes = get_nodes(rows)
            edges = get_edges(nodes)

            G.add_nodes_from(nodes)
            G.add_edges_from(edges)


    return G
