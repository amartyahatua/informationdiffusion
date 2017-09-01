from gensim import corpora
from gensim import corpora, models, similarities



########################################################################################################
############ I/P : Documents. It can be changed to a big file containing many key words of many topics##
############       and one input text, of which we need to find the topic ##############################
############ O/P : Percentage of similarity to every topic with the input text##########################
########################################################################################################




documents = ["Human machine interface for lab abc computer applications",
"A survey of user opinion of computer system response time",
"The EPS user interface management system",
"System and human system engineering testing of EPS",
"Relation of user perceived response time to error measurement",
"The generation of random binary unordered trees",
"The intersection graph of paths in trees",
"Graph minors IV Widths of trees and well quasi ordering",
"Graph minors A survey"]


# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
                for document in documents]


# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)

for text in texts:
     for token in text:
        frequency[token] += 1
        
texts = [[token for token in text if frequency[token] > 1]
        for text in texts]
dictionary = corpora.Dictionary(texts)
dictionary.save('deerwester.dict')
dictionary.token2id





corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('deerwester.mm', corpus)  # store to disk, for later use
#print((corpus))


tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
doc = "Graph theory is important"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
index.save('deerwester.index')
index = similarities.MatrixSimilarity.load('deerwester.index')
sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])


print(sims) 
# corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
# lsi.print_topics(2)


