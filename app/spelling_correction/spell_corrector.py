import json
import numpy as np
import editdistance as ed


# with open('app/corpora/json_corpus.txt', 'r') as tokens:
#     data = json.load(tokens)

def get_all_words(corpus):
    other = ['(', ')', 'and', 'or', 'and_not']
    words = []
    for document in corpus:
        for word in document["title_tokens"]:
            words += [word]
        for word in document["description_tokens"]:
            words += [word]
    words = list(set(words)) 
    words = words + other
    words.sort()
    return words

def get_closest_match(original, word_list):
    #returns 3 closest matches using lev
    if original not in word_list:
        matches = []
        for word in word_list:
            matches.append(ed.eval(original, word))

        a = np.array(matches)
        ind = np.argpartition(a, 3)
        return(word_list[ind[0]])
    else:
        return original

