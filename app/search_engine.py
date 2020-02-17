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


from flask import Flask, render_template, request
from vector_space import vector_space_retrival, weight_calc
from boolean_search import boolean_search
from pre_processing import indexer, preprocessing
from corpus_access import corpus_access
from spelling_correction import spell_corrector
import json
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

with open('app/corpora/inverted_index.txt', 'r') as index:
    uottawa_inverted_index = json.load(index)

with open('app/corpora/uottawa.txt', 'r') as index:
    uottawa_corpus = json.load(index)

with open('app/corpora/json_corpus.txt', 'r') as index:
    uottawa_json_corpus = json.load(index)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=['POST'])
def results():
    try:
        words = spell_corrector.get_all_words(uottawa_json_corpus)
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
            results = corpus_access.convert_doc_ids(query)
            return render_template("results.html", results = results, query=orgQuery)

        elif method == "vector" and collection == "uottawa":
            query = vector_space_retrival.vsm(query, uottawa_inverted_index, uottawa_corpus)
            results = corpus_access.convert_doc_ids(query)
            return render_template("results.html", results=results, query=orgQuery)

        elif method == "boolean" and collection == "other":
            return render_template("under_construction.html")
        elif method == "vector" and collection == "other":
            return render_template("under_construction.html")
    except:
        return render_template("error.html")


    return method

def main():
    
    indexer.create_index()
    weight_calc.calculate_weight()
    app.run(debug=True)

if __name__ == '__main__':
    main()
    

