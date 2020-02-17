import json
import re

with open('app/corpora/json_corpus.txt', 'r') as tokens:
    data = json.load(tokens)

def create_word_bigram(word):
    word = '$' + word + '$'
    word = [word[i:i+2] for i in range(len(word)-1)]
    return word

def get_all_words(corpus):
    words = []
    for document in corpus:
        for word in document["title_tokens"]:
            words += [word]
        for word in document["description_tokens"]:
            words += [word]
    return list(set(words))


def get_all_word_bigrams(word_list):
    word_bigrams = []
    for word in word_list:
        word_bigrams += create_word_bigram(word)
    return list(set(word_bigrams))


def get_matching_words(bigram, word_list):
    matches = []
    if bigram[0] == '$':
        for word in word_list:
            if word.startswith(bigram[1]):
                matches += [word]
    elif bigram[1] == '$':
        for word in word_list:
            if word.endswith(bigram[0]):
                matches += [word]
    else:
        for word in word_list:
            if bigram in word:
                matches += [word]
    return matches


def add_to_index(bigram_list):
    for bigram in bigram_list:
        if bigram in bigram_index:
            new_list = inverted_index[word] + [docID]
            new_list.sort()
            inverted_index[word] = new_list
        else:
            inverted_index[word] = [docID]


def create_bigram_index():
    bigram_index = {}
    words = get_all_words(data)
    bigrams = get_all_word_bigrams(words)
    bigrams.sort()

    for bigram in bigrams:
        bigram_index[bigram] = get_matching_words(bigram, words)


    with open('corpora/bigram_index.txt', 'w') as outfile:
        json.dump(bigram_index, outfile, indent=4, separators=(',', ': '))

#create_bigram_index()
