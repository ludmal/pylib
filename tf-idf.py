#!/usr/bin/python
# -*- coding: latin-1 -*-

import math
from operator import itemgetter

def tfidf(word, doc, docList):
    tf = doc.split(None).count(word) / float(len(doc.split(None)))

    docs_in_word = 0

    for doc in docList:
        if doc.split(None).count(word) > 0:
            docs_in_word +=1

    idf = math.log(len(docList)/ docs_in_word)

    return tf * idf

def top_keywords(doc, docList, n=5):
    d = {}
    for word in set(doc.split(None)):
        d[word] = tfidf(word, doc, docList)

    sorted_d = sorted(d.items(), key=itemgetter(1), reverse=True)
    return [w[0] for w in sorted_d[:n]]
