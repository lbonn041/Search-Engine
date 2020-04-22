from nltk import word_tokenize
import json
import sys
sys.path.append('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/vector_space')
sys.path.append('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/pre_processing')
sys.path.append('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/corpus_access')
from vector_space_retrival import vsm
from weight_calc import calculate_weight
from corpus_access import convert_doc_ids_reuters
from preprocessing_reut import remove_stopwords, token_corpus, lemmetize
from reuter_indexer import create_index

with open('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/corpora/reuters.txt', 'r') as index:
    reuters_corpus = json.load(index)

#get the subset with topics
#that will be training set

def create_set(corpus):
    #returns an array of the documentID that don't and an array of documentID that have a topic

    no_topic = []
    training_set = []

    for document in corpus:
        if len(document['topic']) == 0:
            no_topic.append(document)
        else:
            training_set.append(document)

    return no_topic, training_set

def kNN(documents, training_set, k ):

    tokens = token_corpus(training_set)
    inverted_index = create_index(tokens)
    inverted_index = calculate_weight(inverted_index, training_set)

    for document in documents:
        #get the docID of the document
        docID = int(document['documentID'])
        #process document
        query = (document['description'].lower()).split()
        query = remove_stopwords(query)
        query = lemmetize(query)

        #search for best result
        result = vsm(query, inverted_index, training_set, k)
        result = convert_doc_ids_reuters(result, reuters_corpus)
        topic = [result[0]['topic'][0]]

        reuters_corpus[docID-1]['topic'] = topic
    
    with open('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/corpora/reuters_with_topics.txt', 'w') as outfile:
        json.dump(reuters_corpus, outfile, indent=4, separators=(',', ': '))



no_topic, training_set = create_set(reuters_corpus)
kNN(no_topic, training_set, 1)
