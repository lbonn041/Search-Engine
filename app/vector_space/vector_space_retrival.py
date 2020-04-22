#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

import json
import numpy as np
from math import sqrt


def get_score_query(query, index, N):
    result = {}
    for i in range(1,N+1):
        documentID = str(i)
        score = 0

        for word in query:
            try:
                score += index[word][documentID]
            except:
                score += 0
        try:
            score = score/sqrt(score)

        except ZeroDivisionError:
            score = 0

        result[documentID] = score
    return result

def get_ranking(weightedDict,k):
    sortedDict = {k: v for k, v in sorted(weightedDict.items(), key=lambda item: item[1], reverse = True)}
    return list((sortedDict.keys()))[:k]

def vsm(query, index, corpus, k):
    N = len(corpus)
    scores = get_score_query(query, index, N)
    return get_ranking(scores, k)
