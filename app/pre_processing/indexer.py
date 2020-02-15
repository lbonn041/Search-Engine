import json

with open('app/corpora/json_corpus.txt', 'r') as tokens:
    data = json.load(tokens)

inverted_index = {}


def convert_array(array):
    temp = {}
    for i in array:
        if i in temp:
            temp[i] += 1
        else:
            temp[i] = 1
    return temp


def add_to_index(token_list, docID):
    for word in token_list:
        if word in inverted_index:
            new_list = inverted_index[word] + [docID]
            new_list.sort()
            inverted_index[word] = new_list
        else:
            inverted_index[word] = [docID]


def create_index():
    #
    #   creates index from json input data
    #

    for i in range(len(data)):
        docID = data[i]["documentID"]
        add_to_index(data[i]["title_tokens"], docID)
        add_to_index(data[i]["description_tokens"], docID)

    for doc in inverted_index:
        inverted_index[doc] = convert_array(inverted_index[doc])
    
    with open('app/corpora/inverted_index.txt', 'w') as outfile:
        json.dump(inverted_index, outfile, indent=4, separators=(',', ': '))

#create_index()