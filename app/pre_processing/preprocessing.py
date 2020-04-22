import json
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from bs4 import BeautifulSoup

lemmatizer = WordNetLemmatizer()
def createSoup():
    with open("app/corpora/backup.html", encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, "html.parser")


def remove_stopwords(token_array):
    #
    #   returns an array without the stopwords from the array input of tokens token_array
    #
    punctuation = {",", ".", "'", "'s", ":", ";", "(", ")", "..", '’', '®', '&', '-', '--', '/'}
    stop_words = set(stopwords.words('english'))
    new_token_array = []
    for word in token_array:
        if not((word in stop_words) or (word in punctuation)):
            new_token_array.append(word)
    return new_token_array


def lemmetize(token_array):
    return [lemmatizer.lemmatize(word) for word in token_array]

#creates corpus with tokens
def initialze_corpus(soup): 
    elements = soup.find_all("div", class_="courseblock".split())

    corpus_tokenized = []
    corpus = []
    counter = 1
    for i in elements:

        title = ((i.find('p', class_='courseblocktitle')).text).strip('\n')

        try:
            desc = ((i.find('p', class_='courseblockdesc')).text).strip('\n')

        except AttributeError:
            desc = "N/A"

        if ('\u00e9' in title) or ('\u00e9' in desc):
            continue

        else:
            #store the entire tite and desc in a different doc
            tempDict = {
                "documentID": counter,
                "title": title,
                "description": desc
            }
            corpus.append(tempDict)

            desc_tokens = remove_stopwords(word_tokenize((desc).lower()))
            desc_tokens = lemmetize(desc_tokens)
            title = re.sub(r" \(.*\)", '', title)
            title_tokens = remove_stopwords(word_tokenize((title).lower()))
            title_tokens = lemmetize(title_tokens)

            tempDictToken = {
                "documentID": counter,
                "title_tokens": title_tokens,
                "description_tokens": desc_tokens
            }
            corpus_tokenized.append(tempDictToken)
            counter = counter + 1

    with open('app/corpora/json_corpus.txt', 'w') as outfile1:
        json.dump(corpus_tokenized, outfile1, indent=4, separators=(',', ': '))
    with open('app/corpora/uottawa.txt', 'w') as outfile2:
        json.dump(corpus, outfile2, indent=4, separators=(',', ': '))
