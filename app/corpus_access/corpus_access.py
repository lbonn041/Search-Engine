import json

with open('app/corpora/inverted_index.txt', 'r') as index:
    inverted_index = json.load(index)

with open('app/corpora/uottawa.txt', 'r') as index:
    corpus = json.load(index)

def convert_doc_ids(doc_id_list):
    documents = []
    for documentID in doc_id_list:
        title = corpus[int(documentID) - 1]["title"]
        desc = corpus[int(documentID) - 1]["description"]
        document = {
            "title": title,
            "description": desc
        }
        documents.append(document)
    return documents