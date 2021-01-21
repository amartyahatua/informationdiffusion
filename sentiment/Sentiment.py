import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import json
from blaze.server.serialization import json

########################################################################################################
########## I/P : Text to calculate its sentiment #######################################################
############ O/P : Calculating sentiment using NLTK library and sentiment140 ###########################
########################################################################################################



class Sentiment:
    def getSentimentNLTK(tweetSentence):
        score = []
        try:
            #print('==============getSentimentNLTK starts ====================')
            sid = SentimentIntensityAnalyzer()
            sentimentScore = sid.polarity_scores(tweetSentence)
            score.append(sentimentScore['neu']) 
            score.append(sentimentScore['neg']) 
            score.append(sentimentScore['pos']) 
            score.append(sentimentScore['compound']) 
            #print(tweetSentence)
            #print('score = ',score)
            #print('==============getSentimentNLTK ends ====================')
        except :
            score = [0,0,0,0]
            #print('score = ',score)
        return score    
    
    def getSentimentsentiment140(tweetSentence):
        #print('==============getSentimentsentiment140============')
        try:
            lines_list = tokenize.sent_tokenize(tweetSentence)
            sentence = ''
            for i in range(len(lines_list)):
                sentence = sentence+'+'+lines_list[i] 
            
            qrysentence = 'http://www.sentiment140.com/api/classify?text='+sentence+'&query=new+moon&callback=a'
            sentiQuery = requests.get(qrysentence)
            sentiQuery = sentiQuery.text
            pre = '['
            post = ']'
            sentiQuery = sentiQuery[2:(len(sentiQuery)-2)]
            sentiQuery = pre+sentiQuery+post
            #print(r)
            
            sentiQuery = json.loads(sentiQuery)
            #print(sentiQuery)
            
            sentiScore = sentiQuery[0]['results']['polarity']
            return sentiScore
        except :
            sentiScore = 0
            return  sentiScore





