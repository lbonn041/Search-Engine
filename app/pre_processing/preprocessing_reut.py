from bs4 import BeautifulSoup, SoupStrainer
import json
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def remove_stopwords(token_array):
    punctuation = {",", ".", "'", "'s", ":", ";",
                   "(", ")", "..", '’', '®', '&', '-', '--', '/', '`', '<', '>'}
    stop_words = set(stopwords.words('english'))
    new_token_array = []
    for word in token_array:
        if (word in stop_words) or (word in punctuation) or (word.replace('.', '', 1).isdigit()) or ('\\' in word):
            continue
        else:
            new_token_array.append(word)
    return new_token_array


def lemmetize(token_array):
    return [lemmatizer.lemmatize(word) for word in token_array]


def initialze_corpus(soup):

    corpus = []
    counter = 21001
    elements = soup.find_all('reuters')

    for article in elements:

        #get title
        try:
            title = article.find('title').text
        except:
            title = 'N/A'

        #get topic
        try:
            topics = article.find('topics')
            temp_topic = topics.findAll('d')
            topic = []
            for item in temp_topic:
                item = item.text
                topic.append(item)
        except:
            topic = []

        #get desc
        try:
            desc = article.find('body').text
        except:
            desc = 'N/A'

        #store the entire tite and desc in a different doc
        tempDict = {
            'documentID': counter,
            'topic': topic,
            'title': title,
            'description': desc
        }
        corpus.append(tempDict)


        counter += 1

    with open('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/corpora/reuters.txt', 'a') as outfile:
        json.dump(corpus, outfile, indent=4, separators=(',', ': '))
        

def token_corpus(corpus):

    tokenized_corpus = []

    for document in corpus:

        documentID = document['documentID']
        title = document['title']
        desc = document['description']
        topic = document['topic']


        desc_tokens = remove_stopwords(word_tokenize((desc).lower()))
        desc_tokens = lemmetize(desc_tokens)
        title_tokens = remove_stopwords(word_tokenize((title).lower()))
        title_tokens = lemmetize(title_tokens)

        tempDictToken = {
            "documentID": str(documentID),
            "topic": topic, 
            "title_tokens": title_tokens,
            "description_tokens": desc_tokens
        }
        tokenized_corpus.append(tempDictToken)

    return tokenized_corpus

