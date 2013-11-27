import tf-idf

corpus = []

corpus.append('He became one of basketball’s first YouTube sensations. But basketball primarily exists outside of YouTube. And the coming years will prove Kiwi\'s offline world tougher to navigate.')
corpus.append('Many people say that they enjoy playing chess but quit because of the sheer time commitment it takes to get “good.” It turns out there are many misconceptions about rapidly chess improvement.')
corpus.append('The artist modified an existing 70-year-old homesteader shack by introducing mirrors to create the illusion of transparency, as the structure now takes on the lighting characteristics of anything around it.')

keywords = {}

count = -1
for t in corpus:
    count +=1
    keywords[count] = top_keywords(t, corpus, n=7)

for k,v in keywords.items():
    print k, v
