from flask import Flask, render_template, request
from vector_space import vector_space_retrival, weight_calc
from boolean_search import boolean_search
from pre_processing import indexer
from corpus_access import corpus_access
import json

with open('app/corpora/inverted_index.txt', 'r') as index:
    uottawa_inverted_index = json.load(index)

with open('app/corpora/uottawa.txt', 'r') as index:
    uottawa_corpus = json.load(index)

app = Flask(__name__)


@app.route("/")
def index():
    indexer.create_index()
    weight_calc.calculate_weight()
    return render_template("index.html")

@app.route("/results", methods=['POST'])
def results():
    query = (request.form['search']).lower()
    collection = request.form['collection']
    method = request.form['method']
    if method == "boolean" and collection == "uottawa":
        query = boolean_search.boolean_search(query, uottawa_inverted_index, uottawa_corpus)
        results = corpus_access.convert_doc_ids(query)
        return render_template("results.html", results = results)

    elif method == "vector" and collection == "uottawa":
        query = vector_space_retrival.vsm(query, uottawa_inverted_index, uottawa_corpus)
        results = corpus_access.convert_doc_ids(query)
        return render_template("results.html", results=results)

    elif method == "boolean" and collection == "other":
        return render_template("under_construction.html")
    elif method == "vector" and collection == "other":
        return render_template("under_construction.html")


    return method


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    

