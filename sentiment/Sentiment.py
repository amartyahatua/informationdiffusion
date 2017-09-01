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
        #print('score = ',sentiScore)
        #print(sentiQuery)
# tweetSentence = "It was one of the worst movies I've seen, despite good reviews. \
# ... Unbelievably bad acting!! Poor direction. VERY poor production. \
# ... The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"
#tweet = "Don't buy that. Think Black Wall Street. We need 2 know ourstory. Stop consuming the lies told 2 this country about\xe2\x80\xa6 https://t.co/8I8davZ55v"

#Sentiment.getSentimentsentiment140(tweet)
#getSentimentNLTK(tweetSentence)





