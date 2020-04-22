from nltk import bigrams
import json
from collections import Counter, defaultdict
from nltk.corpus import stopwords


def remove_stopwords(token_array):
    punctuation = {",", ".", "'", "'s", ":", ";",
                   "(", ")", "..", '’', '®', '&', '-', '--', '/'}
    stop_words = set(stopwords.words('english'))
    new_token_array = []
    for word in token_array:
        if not((word in stop_words) or (word in punctuation)):
            new_token_array.append(word)
    return new_token_array


def bigram(corpus):
    model = defaultdict(lambda: defaultdict(lambda: 0))

    for document in corpus:
        title = (remove_stopwords(document['title'].split()))
        for w1, w2 in bigrams(title, pad_right=True, pad_left=True):
            model[w1][w2] += 1
        
        description = (remove_stopwords(document['description'].split()))
        for w1, w2 in bigrams(description, pad_right=True, pad_left=True):
            model[w1][w2] += 1

    for word in model:
        total_count = float(sum(model[word].values()))

        for w2 in model[word]:
            model[word][w2] /= total_count

    with open('app/corpora/bigram_model.txt', 'w') as outfile:
        json.dump(model, outfile, indent=4, separators=(',', ': '))
