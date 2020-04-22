import json

with open('/Users/luc/Documents/GitHub/CSI-4107-Search-Engine-Project/app/corpora/bigram_model_reuters.txt', 'r') as index:
    bigram_model = json.load(index)

def query_completion(bigram_model, words, k):

    if len(words) >= 1:
    
        phrase_suggestion = []

        suggestions = get_most_probable(bigram_model, words[len(words) - 1], k)

        for word in suggestions:
            phrase_suggestion += [' '.join(words[:len(words)]) + ' ' + word]
        
        return phrase_suggestion

    else:
        return []

def get_most_probable(bigram_model, word, k):

    most_probable = []

    sortedDict =  sorted(bigram_model[word].items(), key=lambda item: item[1], reverse=True);

    for i in range(k):
        try:
            most_probable += [sortedDict[i][0]]
        except:
            break
    return most_probable
