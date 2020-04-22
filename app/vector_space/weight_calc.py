import json
import re
import numpy as np
from math import log10


def get_document_frequency(word, inverted_index):
    try:
        return len(inverted_index[word])
    except:
        return 0


def get_tf(word, documentID, inverted_index):
    return inverted_index[word][str(documentID)]

def get_tfidf(word, documentID, inverted_index, corpus):
    N = len(corpus)
    idf =  log10(N/get_document_frequency(word, inverted_index))

    return idf * get_tf(word, documentID, inverted_index)

def calculate_weight(inverted_index, corpus):
    for word in inverted_index:
        weight = {}
        for documentID, value in inverted_index[word].items():
            value = get_tfidf(word, documentID, inverted_index, corpus)
            weight[documentID] = value
        inverted_index[word] = weight

    return inverted_index

