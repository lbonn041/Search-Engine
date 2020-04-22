from nltk.corpus import wordnet, stopwords

stop_words = set(stopwords.words('english'))
punctuation = {",", ".", "'", "'s", ":", ";",
               "(", ")", "..", '’', '®', '&', '-', '--', '/'}

def query_expansion(query, k):
    #expand words in 'query' only if they have less than 'k' definitions
    expanded_query = []

    for word in query:
        new_words = []
        if (word in stop_words) or (word in punctuation):
            new_words += [word]
        else:
            word_defs = wordnet.synsets(word)
            if len(word_defs) > k: 
                #if there is too many definitions, the dont do expansion
                #just add the word to array
                new_words += [word]
            else:
                for word in word_defs:
                    for lemma in word.lemmas():
                        new_words += [lemma.name()]

        expanded_query += new_words
        
    expanded_query = list(set(expanded_query))

    for i in range(len(expanded_query)):
        expanded_query[i] = expanded_query[i].replace('_', ' ')
    return expanded_query


