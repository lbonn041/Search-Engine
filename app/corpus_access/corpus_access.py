import json


def convert_doc_ids(doc_id_list, corpus):
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


def convert_doc_ids_reuters(doc_id_list, corpus):
    documents = []
    for documentID in doc_id_list:
        title = corpus[int(documentID) - 1]["title"]
        desc = corpus[int(documentID) - 1]["description"]
        topic = corpus[int(documentID) - 1]["topic"]
        document = {
            "title": title,
            "description": desc,
            "topic": topic
        }
        documents.append(document)
    return documents

