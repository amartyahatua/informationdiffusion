from gensim import corpora
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

########################################################################################################
############ This program works exactly the same way TopicModeling.py works, only difference in input ##
############ I/P : Documents. 'temp/textTopics.txt' ####################################################
############       and one input text is in 'doc' parameter of topicScore(self, doc) ###################
############ O/P : Percentage of similarity to every topic with the input text##########################
########################################################################################################

class TopicModeling:
    def topicScore(self, doc):
        try:
            text = []
            for line in open('temp/textTopics.txt'):
                         # assume there's one document per line, tokens separated by whitespace
                         stop_words = set(stopwords.words('english'))
                           
                         ## Tokens 
                         word_tokens = word_tokenize(line)
                         # Convert tokens in lower-case 
                         word_tokens = [token.lower() for token in word_tokens]
                         ## Filter tokens
                         filtered_sentence = []
                         for w in word_tokens:
                             if w not in stop_words:
                                 filtered_sentence.append(w)
                         text.append(filtered_sentence)
              
            dictionary = corpora.Dictionary(text)
            dictionary.save('temp/textTopics.dict')  # store the dictionary, for future reference
            corpus = []
            for textWord in text:
                corpus.append(dictionary.doc2bow(textWord))
            corpora.MmCorpus.serialize('temp/textTopics.mm', corpus)  # store to disk, for later use
            lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
            vec_bow = dictionary.doc2bow(doc.lower().split())
            vec_lsi = lsi[vec_bow]
            
            index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
            index.save('temp/textTopics.index')
            index = similarities.MatrixSimilarity.load('temp/textTopics.index')
            sims = index[vec_lsi] 
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            return sims[0:10]
        except:
            sims = [(0,0), (0,0), (0,0), (0,0), (0,0),(0,0), (0,0), (0,0), (0,0), (0,0)]
            return sims
        pos = arange(len(sims))+.5    # the bar centers on the y axis
        figure(1)
        barh(pos,sims, align='center')
        yaxis = []
        # ## Create yaxis labels 
        for i in range(len(sims)):
             label = 'Topic '
             label = label + str(i)
             yaxis.append(label)
         
         
        
        
        yticks(pos, yaxis)
        xlabel('Performance')
        title('Toopic Modeling')
        grid(True)
        show()





