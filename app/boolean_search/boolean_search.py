import json
import re


def infixToPostfix(infixexpr):
    prec = {}
    prec["and_not"] = 2
    prec["and"] = 2
    prec["or"] = 2
    prec["("] = 1
    opStack = []
    postfixList = []

    for token in infixexpr:
        if not ((token == "and") or (token == "or") or (token == "and_not") or (token == ")") or (token == "(")):
            postfixList.append(token)
        elif token == '(':
            opStack += [token]
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not len(opStack) == 0) and (prec[opStack[len(opStack)-1]] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.append(token)

    while not (len(opStack) == 0):
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def postfixEval(postfixExpr, index, corpus):
    operandStack = []
    infixexpr = postfixExpr.split()

    for token in infixexpr:
        if not ((token == "and") or (token == "or") or (token == "and_not")):
            operandStack += [token]
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(token, operand1, operand2, index, corpus)
            operandStack += [result]
    return operandStack.pop()


def doMath(op, op1, op2, index, corpus):
    if op == "and":
        return and_query(op1, op2, index)
    elif op == "and_not":
        return and_not_query(op1, op2, index, corpus)
    elif op == "or":
        return list(set(get_docIDs(op1, index) + get_docIDs(op2, index)))


def get_docIDs(word, index):
    documentIDs = []
    if type(word) == list:
        return word
    try :
        if '*' in word:
            word_split = word.split("*")
            for key in index:
                if bool(re.match(word_split[0]+'(.+?)'+word_split[1], key)):
                    for key in index[key]:
                        documentIDs += [int(key)]
            return documentIDs
        else:
            for key in index[word]:
                documentIDs += [int(key)]
            return documentIDs
    except:
        return []


def and_query(op1, op2, index):
    list1, list2 = get_docIDs(op1, index), get_docIDs(op2, index)
    answer = []
    i,j = 0,0
    while (i != len(list1) and (j != len(list2))):
        if list1[i] == list2[j]:
            answer.append(list1[i])
            i = i + 1
            j = j + 1

        elif list1[i] < list2[j]:
            i = i + 1

        else:
            j = j + 1
            
    return answer


def and_not_query(op1, op2, index, corpus):
    ALL_DOCS = []
    for i in range(len(corpus)):
        ALL_DOCS += [i]
    
    list1, list2 = get_docIDs(op1, index), list(set(ALL_DOCS)^set(get_docIDs(op2, index)))
    answer = []
    i, j = 0, 0
    while (i != len(list1) and (j != len(list2))):
        if list1[i] == list2[j]:
            answer.append(list1[i])
            i = i + 1
            j = j + 1

        elif list1[i] < list2[j]:
            i = i + 1

        else:
            j = j + 1
    return answer

def boolean_search(query, index, corpus):
    if len(query) == 1:
        return get_docIDs(query[0], index)
    else:
        query = infixToPostfix(query)
        return postfixEval(query, index, corpus)

    
