# Content recommendations with wikipedia graph data

Can we use wikipedia graph data to create content recommendations?

# How it works

1. Identify entities in a piece of content
2. Find vector representations for entities from wikipedia
3. The piece of content takes the mean value of the entities in that bit of content
4. Use nearest neighbours to identify some possibly related bits of content

## BBC content dataset

There's an dataset that contains 2225 documents from the BBC.

http://mlg.ucd.ie/datasets/bbc.html

## Named Entity Recognition

Named entity recognition (NER) is the process of identifying parts of a bit of text that identify a thing. This is a natural language processing technique.

I've used spacy to perform the named entity recognition. This is an open source industrial strength NLP library.

https://spacy.io/usage/linguistic-features

## Wikipedia2vec

Wikipedia2vec is a project that creates vector representations of entities in wikipedia.

https://wikipedia2vec.github.io/wikipedia2vec/


# Training

Extract the entities using NLP from spacy:

```
python run.py --extract
```


Get the vector representations for each bit of content:

```
python run.py --vectorise
```

# Running

Run a simple flask webapp that gives you the nearest neighbours of a bit of content.

```
export FLASK_APP=contentgraph/serve.py

flask run
```

# Possible things to try

## Contribute to NER

Spacy lets you expand the NER through applying more rules and retraining.

https://spacy.io/usage/linguistic-features#updating

## More sophisticated Named Entity Linking

I link between entities and wikipedia2vec in a very naive way,
just looking for exact matches. So the spelling, the case of the text, any abbreviation needs to be exactly the same.

Named entity linking is a field that gives you more sophisticated approaches to this.

## Other graph embeddings

Wikipedia2vec is using a skipgram technique to learn the embeddings of the entity graph. Other methods are available for determining the embeddings of a graph.

## Other nearest neighbour methods

I've just used the vanilla nearest neighbour method from [annoy](https://github.com/spotify/annoy). Other methods for finding related vectors might be interesting to play with.

I've also taken the mean value for each bit of content and then fed that into the nearest neighbours. I'm not sure if that's smart, or if it would be better to take the entities themselves and then do nearest neighbours.
