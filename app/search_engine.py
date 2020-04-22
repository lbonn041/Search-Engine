######
#   LUC-CYRIL BONNET 8234136
#   MELODY HABBOUCHE 8305782
#
#   LIST OF SOURCES USED:
#   https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
#   https://codereview.stackexchange.com/questions/223772/python-calculator-using-postfix-expressions
#   Intersect algorithm from lecture notes
#
#
######


from flask import Flask, render_template, request, jsonify
from vector_space import vector_space_retrival
from boolean_search import boolean_search
from pre_processing import indexer, preprocessing
from corpus_access import corpus_access
from spelling_correction import spell_corrector
from query_expansion import query_expansion
from query_completion import query_completion
import json
from nltk.stem.wordnet import WordNetLemmatizer
import sys

lemmatizer = WordNetLemmatizer()

with open('app/corpora/inverted_index_uottawa.txt', 'r') as index:
    uottawa_inverted_index = json.load(index)

with open('app/corpora/uottawa.txt', 'r') as index:
    uottawa_corpus = json.load(index)

with open('app/corpora/uottawa_tokens.txt', 'r') as index:
    uottawa_tokens = json.load(index)

with open('app/corpora/inverted_index_reuters.txt', 'r') as index:
    reuters_inverted_index = json.load(index)

with open('app/corpora/reuters_with_topics.txt', 'r') as index:
    reuters_corpus = json.load(index)

with open('app/corpora/reuters_tokens.txt', 'r') as index:
    reuters_tokens = json.load(index)

with open('app/corpora/bigram_model_reuters.txt', 'r') as index:
    bigram_reuters = json.load(index)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/autocomplete', methods=['POST','GET'])
def autocomplete():

    orgQuery = (request.form['query'])
    query = orgQuery.lower().split(" ")
    #print(query)
    comp = query_completion.query_completion(bigram_reuters,query,3)
    print(comp)

    return jsonify(json_list=comp)


@app.route("/results", methods=['POST'])
def results():
    try:
        words = spell_corrector.get_all_words(uottawa_tokens)
        words += spell_corrector.get_all_words(reuters_tokens)
        orgQuery = (request.form['search'])
        query = orgQuery.lower().split(" ")
        collection = request.form['collection']
        method = request.form['method']


        #spell correction
        for i in range(len(query)):
            if '*' in query[i]:
                pass
            else:
                query[i] = spell_corrector.get_closest_match(query[i], words)
                query[i] = lemmatizer.lemmatize(query[i])


        if method == "boolean" and collection == "uottawa":
            query = boolean_search.boolean_search(query, uottawa_inverted_index, uottawa_corpus)
            results = corpus_access.convert_doc_ids(query, uottawa_corpus)
            return render_template("results.html", results = results, query=orgQuery)

        elif method == "vector" and collection == "uottawa":
            query = vector_space_retrival.vsm(query, uottawa_inverted_index, uottawa_corpus,15)
            results = corpus_access.convert_doc_ids(query, uottawa_corpus)
            return render_template("results.html", results=results, query=orgQuery)

        elif method == "boolean" and collection == "reuters":
            query = boolean_search.boolean_search(query, reuters_inverted_index, reuters_corpus)
            results = corpus_access.convert_doc_ids(query, reuters_corpus)
            return render_template("results.html", results = results, query=orgQuery)


        elif method == "vector" and collection == "reuters":
            query = vector_space_retrival.vsm(query, reuters_inverted_index, reuters_corpus, 15)
            results = corpus_access.convert_doc_ids(query, reuters_corpus)
            return render_template("results.html", results=results, query=orgQuery)

    except:
        return render_template("error.html")

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    

