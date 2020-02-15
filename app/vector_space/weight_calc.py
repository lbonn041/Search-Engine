import json
import re
import numpy as np
from math import log10


with open('app/corpora/inverted_index.txt', 'r') as index:
    inverted_index = json.load(index)
    index.close()

with open('app/corpora/json_corpus.txt', 'r') as index:
    corpus = json.load(index)

def get_document_frequency(word):
    try:
        return len(inverted_index[word])
    except:
        return 0


def get_tf(word, documentID):
    return inverted_index[word][str(documentID)]

def get_tfidf(word, documentID):
    N = len(corpus)
    idf =  log10(N/get_document_frequency(word))

    return idf * get_tf(word,documentID)

def calculate_weight():
    for word in inverted_index:
        weight = {}
        for documentID, value in inverted_index[word].items():
            value = get_tfidf(word, documentID)
            weight[documentID] = value
        inverted_index[word] = weight

        

    with open('app/corpora/inverted_index.txt', 'w') as index:
        json.dump(inverted_index, index, indent=4, separators=(',', ': '))
        index.close()

#calculate_weight()
