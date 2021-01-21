
from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import csv
import json
import datetime
from datetime import datetime
from email.utils import parsedate
from collections import defaultdict
import re
import sys
import oauth2 as oauth
import os.path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import topicModeling2_wiki as tp 

MAX_LOC_COLS_NUM = 10;
MAX_LANG_COLS_NUM = 20;
MAX_USERS_COLS_NUM = 20;
MAX_HASHTAGS_COLS_NUM = 20;

class SentimentAnalysis:
    def getSentimentNLTK(self, tweetSentence):
        score = []
        tweetSentence = str(tweetSentence)
        tweetSentence = tweetSentence[2:len(tweetSentence)-2]
        sid = SentimentIntensityAnalyzer()
        sentimentScore = sid.polarity_scores(tweetSentence)
        score.append(sentimentScore['neu']) 
        score.append(sentimentScore['neg']) 
        score.append(sentimentScore['pos']) 
        score.append(sentimentScore['compound']) 
        return score
    def getSentimentsentiment140(self, tweetSentence):
        #print('==============getSentimentsentiment140============')
        tweetSentence = str(tweetSentence)
        tweetSentence = tweetSentence[2:len(tweetSentence)-2]
        lines_list = tokenize.sent_tokenize(tweetSentence)
        sentence = ''
        for i in range(len(lines_list)):
            sentence = sentence+'+'+lines_list[i] 
        
        qrysentence = 'http://www.sentiment140.com/api/classify?text='+sentence+'&query=new+moon&callback=a'
        sentiQuery = requests.get(qrysentence)
        sentiQuery = sentiQuery.text
        
        if(sentiQuery.startswith('a({"results":')):
            pre = '['
            post = ']'
            sentiQuery = sentiQuery[2:(len(sentiQuery)-2)]
            sentiQuery = pre+sentiQuery+post
            sentiQuery = json.loads(sentiQuery)
            sentiScore = sentiQuery[0]['results']['polarity']
            return sentiScore
        else:
            sentiScore = 2
            return sentiScore
    
    
    
    
class UserProfile:
    def __init__(self):
        self.consumer_key="xxxxxxxxxxxx"
        self.consumer_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        self.access_token="xxxxxxxxxxxx"
        self.access_token_secret="xxxxxxxxxxxx"

        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)        
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        
        self.oconsumer = oauth.Consumer(key=self.consumer_key,secret=self.consumer_secret)
        self.oaccess_token = oauth.Token(key=self.access_token,secret=self.access_token_secret)
        self.client = oauth.Client(self.oconsumer,self.oaccess_token)
        
        self.screenNameList = []
        
        self.idlist = []
        self.screen_name = []
        self.default_profile_image = []
        self.statuses_count = []
        self.profile_use_background_image = []
        self.profile_link_color = []
        self.profile_background_color = []
        self.profile_text_color = []
        self.verified = []
        self.favourites_count = []
        self.utc_offset = []
        self.is_translation_enabled= []
        self.followers_count = []
        self.description = []
        self.created_at = []
        self.listed_count = []
        self.friends_count = []
        self.follow_request_sent = []
        self.translator_type = []
        self.following = []
        self.default_profile = []
        self.notifications = []
        self.location = [] 
        self.time_zone = []
        self.geo_enabled = []
        self.lang = []
        self.protected = []
        self.has_extended_profile = []
        self.profile_use_background_image = []
        self.default_profile_image = []
        self.langIndex = []
        
    def getLanguageList(self, listOfLan):
        #listOfLan = ['en','ar','cs']
        languageIndexList = []
        languageList = ['en','ar','bn','cs','da','de','el','es','fa','fi','fil','fr','he','hi','hu','id','it','ja','ko','msa','nl','no','pl','pt','ro','ru','sv','th','tr','uk','ur','vi','zh-cn','zh-tw']
        #print(len(listOfLan))
        for i in range(len(listOfLan)):
            languageIndexList.append(languageList.index(listOfLan[i]))
              
        return languageIndexList

    def remove_comma(self, text):
        word_search = ','
        result_text = ''
        if word_search in text:
            result_text = text.replace(',', ' ')
        else:
            result_text = text
        return result_text
        
    def remove_b(self, text):
        result_text = ''
        if text.startswith('b'):
            result_text = text[1:]
        else:
            result_text = text
        return result_text
    
    def isEnglish(self, s):
        if re.match("^[A-Za-z0-9_-]*$", s):
            return 1
        else:
            return 0
    
    def convertToDec(self, input):
        result = 0
        pre = '0x'
        input = pre+input
        result = int(input, 16)
        return result
    
    def readScreenNameList(self, fileName):
        #'C:\\Users\\ahatua\\Desktop\\1.csv'
        with open(fileName) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                self.screenNameList.append(row[0])
    
    def analyzeUserProfile(self, screen_name):
        userDeatilsRequestURL = "https://api.twitter.com/1.1/users/lookup.json?screen_name=" + screen_name
        response, data = self.client.request(userDeatilsRequestURL)  
        my_json = data.decode('utf8')        
        my_json = json.loads(my_json)
        word = 'errors'
        if word in my_json:
            print('Error')
        else:
            self.idlist.append((my_json[0]['id']))
            self.screen_name.append(str(my_json[0]['screen_name']))            
            
            if my_json[0]['default_profile_image']:
                self.default_profile_image.append(1)
            else:
                self.default_profile_image.append(0)
            self.statuses_count.append(str(my_json[0]['statuses_count']))
            
            if my_json[0]['profile_use_background_image']:
                self.profile_use_background_image.append(1)
            else:
                self.profile_use_background_image.append(0)
            
            self.profile_link_color.append(self.convertToDec(str(my_json[0]['profile_link_color'])))
            self.profile_background_color.append(self.convertToDec(str(my_json[0]['profile_background_color'])))
            self.profile_text_color.append(self.convertToDec(str(my_json[0]['profile_text_color'])))
                        
            if my_json[0]['verified']:
                self.verified.append(1)
            else:
                self.verified.append(0)
            
            self.favourites_count.append(str(my_json[0]['favourites_count']))
            self.utc_offset.append(str(my_json[0]['utc_offset']))
            
            if my_json[0]['is_translation_enabled']:
                self.is_translation_enabled.append(1)
            else:
                self.is_translation_enabled.append(0)
            
            self.followers_count.append(str(my_json[0]['followers_count']))
            self.description.append(my_json[0]['description'])
            self.created_at.append(str(my_json[0]['created_at']))
            self.listed_count.append(str(my_json[0]['listed_count']))
            self.friends_count.append(str(my_json[0]['friends_count']))
            
            if my_json[0]['follow_request_sent']:
                self.follow_request_sent.append(1)
            else:
                self.follow_request_sent.append(0)
                       
            if 'none' in my_json[0]['translator_type']:
                self.translator_type.append(0)
            else: 
                self.translator_type.append(1)
            
            if my_json[0]['following']:
                self.following.append(1)
            else:
                self.following.append(0)            
            
            if my_json[0]['default_profile']:
                self.default_profile.append(1)
            else:
                self.default_profile.append(0)
            
            if my_json[0]['notifications']:
                self.notifications.append(1)
            else:
                self.notifications.append(0)
            
            if my_json[0]['location'] is None:
                self.location.append('none')
            else:
                if (self.isEnglish(my_json[0]['location']) == 1):
                    location_string = str(my_json[0]['location'])
                    self.location.append(location_string)
                else:
                    self.location.append('none')
                    
            self.time_zone.append(str(my_json[0]['time_zone']))
            
            if my_json[0]['geo_enabled']:
                self.geo_enabled.append(1)
            else:
                self.geo_enabled.append(0)
                
            if my_json[0]['protected']:
                self.protected.append(1)
            else:
                self.protected.append(0)
            
            if my_json[0]['has_extended_profile']:
                self.has_extended_profile.append(1)
            else: 
                self.has_extended_profile.append(0)
            
            self.lang.append(str(my_json[0]['lang']))
            self.langIndex = self.getLanguageList(self.lang)
            
    def exportCSV(self, outFileName, lstStatsColNames, lstUserStats):

        with open(outFileName,'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
            lstCols = ["id","screen_name","default_profile_image","statuses_count","profile_use_background_image","profile_link_color",
                             "profile_background_color","profile_text_color","verified","favourites_count","utc_offset","is_translation_enabled",
                             "followers_count","created_at","listed_count","friends_count","follow_request_sent","translator_type","following",
                             "default_profile","notifications","location","time_zone","geo_enabled","lang","protected","has_extended_profile",
                             "profile_use_background_image","default_profile_image"]
            if(lstStatsColNames is not None):
                lstCols.extend(lstStatsColNames)
            writer.writerow(lstCols)
            rows = zip(self.idlist,self.screen_name,self.default_profile_image,self.statuses_count,self.profile_use_background_image,
                       self.profile_link_color,self.profile_background_color,self.profile_text_color,self.verified,self.favourites_count,self.utc_offset,
                       self.is_translation_enabled,self.followers_count,self.created_at,self.listed_count,self.friends_count,self.follow_request_sent,
                       self.translator_type,self.following,self.default_profile,self.notifications,self.location,self.time_zone,self.geo_enabled,
                       self.langIndex,self.protected,self.has_extended_profile,self.profile_use_background_image,self.default_profile_image)
            dataRows = []
            if(lstUserStats is not None):
                i = 0
                for row in rows:
                    rowData = list(row)
                    rowData.extend(lstUserStats[i])
                    dataRows.append(rowData)
                    i += 1
            try:  
                for rowData in dataRows:    
                    writer.writerow(rowData)
            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            except ValueError:
                print ("Could not convert data to an integer.")
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                                
class UserTweetStats:
    def __init__(self, screen_name):

        self.screen_name = screen_name
        #alltweets = get_all_tweets(screen_name)
        # Go to http://apps.twitter.com and create an app.
        # The consumer key and secret will be generated for you after
        self.consumer_key="xxxxxxxxxxxxxxxxxxx"
        self.consumer_secret="xxxxxxxxxxxxxxxxxxx"

        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        self.access_token="xxxxxxxxxxxxxxxxxxx"
        self.access_token_secret="xxxxxxxxxxxxxxxxxxx"

        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret) 
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        
        self.nTotalTweets = 0  #total tweets
        self.nTotalRetweets = 0
        #quote status
        self.nTotalQuoteStatus = 0
        #mentioned in tweet
        self.nTotalMentionedTweets = 0
        self.nTotalMentionedRetweets = 0
        #in reply to xxx
        self.nTotalInReplyTweets = 0
        #favorited tweets or not
        self.nTotalFavoritedTweets = 0
        self.nTotalFavorites = 0
        #coordinated
        self.nTotalNotNullCoordinates = 0
        self.nTotalNullCoordinates = 0
        #truncated or not
        self.nTotalTruncated = 0
        self.nTotalNotTruncated = 0
        #contributors
        self.nTotalNullContributors = 0
        self.nTotalNotNullContributors = 0
        #possible sensitive
        self.nTotalPossibleSensitive = 0
        self.nTotalNotPossibleSensitive = 0
        #geo
        self.nTotalNullGeo = 0
        self.nTotalNotNullGeo = 0
        #location
        self.nTotalNullPlace = 0
        self.nTotalNotNullPlace= 0
        self.arrTopLocation = defaultdict(int)
        #Url, image, video in tweets
        self.nRatioUrlInTweets = 0
        self.nTotalUrlInTweets = 0
        self.nRatioImageInTweets = 0
        self.nTotalImageInTweets = 0
        self.nRatioVideoInTweets = 0
        self.nTotalVideoInTweets = 0
        self.nRatioSymbolInTweets = 0
        self.nTotalSymbolInTweets = 0
        #language of tweets
        self.nTotalLang = 0
        self.arrTopLang = defaultdict(int)
        
        # Sentiment scores 
        self.sentimentScore = []
        
        #Tweets frequency
        self.nAge = 0    #number of months from created
        self.arrTweetTimeFrequency = defaultdict(int)
        for i in range(6):
            self.arrTweetTimeFrequency[i] = 0
        self.arrTweetDayFrequency = defaultdict(int)
        for i in range(7):
            self.arrTweetDayFrequency[i] = 0
        self.arrTweetWeekFrequency = defaultdict(int)
        for i in range(53):
            self.arrTweetWeekFrequency[i] = 0
        self.arrTweetMonthFrequency = defaultdict(int)
        for i in range(12):
            self.arrTweetMonthFrequency[i] = 0
        #Retweets frequency
        self.arrRetweetTimeFrequency = defaultdict(int)
        for i in range(6):
            self.arrRetweetTimeFrequency[i] = 0
        self.arrRetweetDayFrequency = defaultdict(int)
        for i in range(7):
            self.arrRetweetDayFrequency[i] = 0
        self.arrRetweetWeekFrequency = defaultdict(int)
        for i in range(53):
            self.arrRetweetWeekFrequency[i] = 0
        self.arrRetweetMonthFrequency = defaultdict(int)
        for i in range(12):
            self.arrRetweetMonthFrequency[i] = 0
        #Tweet time frequency for different 4 types of source: FB, Android, Iphone, others
        self.arrTweetFBTimeFrequency = defaultdict(int)
        for i in range(24):
            self.arrTweetFBTimeFrequency[i] = 0
        
        self.arrTweetAndroidTimeFrequency = defaultdict(int)
        for i in range(24):
            self.arrTweetAndroidTimeFrequency[i] = 0
        
        self.arrTweetIphoneTimeFrequency = defaultdict(int)
        for i in range(24):
            self.arrTweetIphoneTimeFrequency[i] = 0
        
        self.arrTweetOtherTimeFrequency = defaultdict(int)
        for i in range(24):
            self.arrTweetOtherTimeFrequency[i] = 0
        #Mentioned users
        self.nTotalMentionedUsers = 0
        self.arrMentionedUsers = defaultdict(int)
        #Hashtags
        self.nTotalHastags = 0
        self.arrTopHastags = defaultdict(int)
        #Trending topics
        self.nTotalInTrending = 0
        #######################################
    def print(self):
        print('Total Tweets:', self.nTotalTweets)
        print('Total ReTweets:', self.nTotalRetweets)
        print('Total Quote Status:', self.nTotalQuoteStatus)
        print('Total Mentioned Tweets:', self.nTotalMentionedTweets)
        print('Total Mentioned Retweets:', self.nTotalMentionedRetweets)
        print('Total In Reply Tweets:', self.nTotalInReplyTweets)
        print('Total Favorited Tweets:', self.nTotalFavoritedTweets)
        print('Total Favorite Count:', self.nTotalFavorites)
        print('Total Null Coordinates:', self.nTotalNullCoordinates)
        print('Total Not Null Coordinates:', self.nTotalNotNullCoordinates)
        print('Total Truncated Tweets:', self.nTotalTruncated)
        print('Total Not Truncated Tweets:', self.nTotalNotTruncated)
        print('Total Null Contributors:', self.nTotalNullContributors)
        print('Total Not Null Contributors:', self.nTotalNotNullContributors)
        print('Total Possible Sensitive:', self.nTotalPossibleSensitive)
        print('Total Not Possible Sensitive:', self.nTotalNotPossibleSensitive)
        print('Total Null Geo:', self.nTotalNullGeo)
        print('Total Not Null Geo:', self.nTotalNotNullGeo)
        print('Total Null Place:', self.nTotalNullPlace)
        print('Total Not Null Place:', self.nTotalNotNullPlace)
        print('List top place:', self.arrTopLocation)
        #Url, image, video in tweets        
        print('Ratio Url In Tweets:', self.nRatioUrlInTweets)
        print('Total Url In tweets:', self.nTotalUrlInTweets)    
        print('Ratio Image In Tweets:', self.nRatioImageInTweets)
        print('Total Image In tweets:', self.nTotalImageInTweets)
        print('Ratio Video In Tweets:', self.nRatioVideoInTweets)
        print('Total Video In tweets:', self.nTotalVideoInTweets)
        print('Ratio Symbol In Tweets:', self.nRatioSymbolInTweets)
        print('Total Symbol In tweets:', self.nTotalSymbolInTweets)
        #language of tweets
        print('Total Language:', self.nTotalLang)
        print('List top language:', self.arrTopLang)
        #Tweets frequency
        for key in self.arrTweetTimeFrequency:
            print('Tweet Time frequency %d-%d: %d' % (key*4+1, key*4+4, self.arrTweetTimeFrequency[key]))
        for key in self.arrTweetDayFrequency:
            print('Tweet weekday frequency %d: %d' % (key, self.arrTweetDayFrequency[key]))
        for key in self.arrTweetWeekFrequency:
            print('Tweet weeknum frequency %d: %d' % (key, self.arrTweetWeekFrequency[key]))
        for key in self.arrTweetMonthFrequency:
            print('Tweet month frequency %d: %d' % (key, self.arrTweetMonthFrequency[key]))
        #Retweets frequency
        for key in self.arrRetweetTimeFrequency:
            print('Retweet Time frequency %d-%d: %d' % (key*4+1, key*4+4, self.arrRetweetTimeFrequency[key]))
        for key in self.arrRetweetDayFrequency:
            print('Retweet weekday frequency %d: %d' % (key, self.arrRetweetDayFrequency[key]))
        for key in self.arrRetweetWeekFrequency:
            print('Retweet weeknum frequency %d: %d' % (key, self.arrRetweetWeekFrequency[key]))
        for key in self.arrRetweetMonthFrequency:
            print('Retweet month frequency %d: %d' % (key, self.arrRetweetMonthFrequency[key]))
        #Mentioned users
        print('Total Mentioned Users:', self.nTotalMentionedUsers)
        print('List Mentioned Users:', self.arrMentionedUsers)
        #Hashtags
        print('Total Hashtags In Tweets:', self.nTotalHastags)
        print('List Hashtags In tweets:', self.arrTopHastags)
        #Trending topics
        print(self.nTotalInTrending)
    def get_all_tweets(self, screen_name):
        alltweets = []
        
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name = screen_name,count=200)
        if (len(new_tweets) > 0):
            #save most recent tweets
            alltweets.extend(new_tweets)    
            #save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
    
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
    
            if (len(new_tweets) > 0):
                #save most recent tweets
                alltweets.extend(new_tweets)
                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1
    
            print("...%s tweets downloaded so far" % (len(alltweets)) )
    
        #transform the tweepy tweets into a 2D array that will populate the csv    
        outtweets = [tweet._json for tweet in alltweets]
        
        #write the json
        with open('%s_tweets.json' % screen_name, 'w') as f:        
            f.write(json.dumps(outtweets))    
        pass
        
        return alltweets
    def loadAllJsonTweets(self, fileName):
        with open(fileName) as data_file:    
            data = json.load(data_file) 
        return data
    def analyzeUserEntities(self, tweet):
        entities = tweet['entities']
        lstMentionedUsers = entities.get('user_mentions',[])
        if(len(lstMentionedUsers) > 0):
            self.nTotalMentionedTweets += 1
            if(tweet.get('retweeted_status', 'null') != 'null'): 
                self.nTotalMentionedRetweets += 1
        for mentioned_user in lstMentionedUsers:            
            self.nTotalMentionedUsers += 1
            if mentioned_user['screen_name'] in self.arrMentionedUsers:
                self.arrMentionedUsers[mentioned_user['screen_name']] += 1
            else:
                self.arrMentionedUsers[mentioned_user['screen_name']] = 1

        if(len(entities['urls']) > 0):
            self.nRatioUrlInTweets += 1
            self.nTotalUrlInTweets += len(entities['urls'])

        lstMedia = entities.get('media', [])    
        if(len(lstMedia) > 0):
            tw_has_photo = False
            tw_has_video = False
            for media_element in lstMedia:
                if(media_element['type'] == 'photo'):
                    tw_has_photo = True
                    self.nTotalImageInTweets += 1
                else:
                    tw_has_video = True
                    self.nTotalVideoInTweets += 1
            if(tw_has_photo):
                self.nRatioImageInTweets += 1
            if(tw_has_video):
                self.nRatioVideoInTweets += 1        

        if(len(entities['symbols']) > 0):
            self.nRatioSymbolInTweets += 1
            self.nTotalSymbolInTweets += len(entities['symbols'])

        if(len(entities['hashtags']) > 0):
            self.nTotalHastags += 1
        for hash_tags in entities['hashtags']:
            self.arrTopHastags[hash_tags['text']] += 1

    def analyzeUserTweetTime(self, tweet):
        if(tweet['created_at'] is not None):

            created_at = datetime(*(parsedate(tweet['created_at'])[:6]))
            #Hour
            if(0 <= created_at.hour & created_at.hour < 4):
                self.arrTweetTimeFrequency[0] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[0] += 1
            elif (4 <= created_at.hour & created_at.hour < 8):
                self.arrTweetTimeFrequency[1] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[1] += 1
            elif (8 <= created_at.hour & created_at.hour < 12):
                self.arrTweetTimeFrequency[2] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[2] += 1
            elif (12 <= created_at.hour & created_at.hour < 16):
                self.arrTweetTimeFrequency[3] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[3] += 1
            elif (16 <= created_at.hour & created_at.hour < 20):
                self.arrTweetTimeFrequency[4] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[4] += 1
            elif (20 <= created_at.hour & created_at.hour < 24):
                self.arrTweetTimeFrequency[5] += 1
                if(hasattr(tweet, 'retweeted_status')):            
                    self.arrRetweetTimeFrequency[5] += 1
            #Week Day
            weekDay = created_at.isocalendar()[2]
            self.arrTweetDayFrequency[weekDay-1] += 1
            if(hasattr(tweet, 'retweeted_status')):            
                self.arrRetweetDayFrequency[weekDay-1] += 1
            #Week Number
            weekNum = created_at.isocalendar()[1]
            self.arrTweetWeekFrequency[weekNum-1] += 1
            if(hasattr(tweet, 'retweeted_status')):            
                self.arrRetweetWeekFrequency[weekNum-1] += 1
            #Month
            self.arrTweetMonthFrequency[created_at.month-1] += 1
            if(hasattr(tweet, 'retweeted_status')):            
                self.arrRetweetMonthFrequency[created_at.month-1] += 1
            #source property
            src = tweet['source']
            if('Facebook' in src):
                self.arrTweetFBTimeFrequency[created_at.hour] += 1
            elif('Android' in src):
                self.arrTweetAndroidTimeFrequency[created_at.hour] += 1
            elif('Iphone' in src):
                self.arrTweetIphoneTimeFrequency[created_at.hour] += 1
            else:
                self.arrTweetOtherTimeFrequency[created_at.hour] += 1

    def analyze(self, alltweets):

        i = 0
        for tweet in alltweets:
            i += 1

            
            if(tweet.get('text', 'null') != 'null'): 
                textOfTweet = tweet['text']
                tp.getModel(textOfTweet)

            if(tweet.get('retweeted_status', 'null') != 'null'): 
                self.nTotalRetweets += 1

            if(tweet.get('is_quote_status', False)):
                self.nTotalQuoteStatus += 1

            if(tweet['in_reply_to_user_id'] is not None):
                self.nTotalInReplyTweets += 1

            if(tweet.get('favorited', False)):
                self.nTotalFavoritedTweets += 1
            self.nTotalFavorites += tweet['favorite_count']

            if(tweet['coordinates'] is None):
                self.nTotalNullCoordinates += 1
            else:
                self.nTotalNotNullCoordinates += 1

            if(tweet.get('truncated', False)):
                self.nTotalTruncated += 1
            else:
                self.nTotalNotTruncated += 1

            if(tweet['contributors'] is None):
                self.nTotalNullContributors += 1
            else:
                self.nTotalNotNullContributors += 1
         
            if(tweet.get('possibly_sensitive', False)):
                self.nTotalPossibleSensitive += 1
            else:
                self.nTotalNotPossibleSensitive += 1

            if(tweet['geo'] is None):
                self.nTotalNullGeo += 1
            else:
                self.nTotalNotNullGeo += 1

            if(tweet['place'] is None):
                self.nTotalNullPlace += 1
            else:
                self.nTotalNotNullPlace += 1
                if tweet['place']['id'] in self.arrTopLocation:
                    self.arrTopLocation[tweet['place']['id']] += 1
                else:
                    self.arrTopLocation[tweet['place']['id']] = 1

            if(tweet['lang'] is not None):                
                if tweet['lang'] in self.arrTopLang:
                    self.arrTopLang[tweet['lang']] += 1
                else:
                    self.arrTopLang[tweet['lang']] = 1
                self.nTotalLang = len(self.arrTopLang)

            self.analyzeUserEntities(tweet)
            self.analyzeUserTweetTime(tweet)
            
    def exportArrToDelim(self, arr, lstItems, needSort, maxItem, defaultItem):
        if(needSort):
            sorted_arr = sorted(arr, key=arr.get, reverse=True)
        else:
            sorted_arr = arr
        i = 0
        for v in sorted_arr:
            if(i < maxItem):
                lstItems.append(arr[v])
                i += 1
            else:
                break
        while i < maxItem:
            lstItems.append(defaultItem)
            i += 1
    def getFeaturesNames(self, bIncludeUserId, bIncludeScreenName):
        lstColNames = []
        if(bIncludeUserId):
            lstColNames.append('userid')
        if(bIncludeScreenName):
            lstColNames.append('screen_name')        
        lstColNames.append('nTotalTweets')
        lstColNames.append('nTotalRetweets')
        lstColNames.append('nTotalQuoteStatus')
        lstColNames.append('nTotalMentionedTweets')
        lstColNames.append('nTotalMentionedRetweets')
        lstColNames.append('nTotalInReplyTweets')
        lstColNames.append('nTotalFavoritedTweets')
        lstColNames.append('nTotalFavorites')
        lstColNames.append('nTotalNullCoordinates')
        lstColNames.append('nTotalNotNullCoordinates')
        lstColNames.append('nTotalTruncated')
        lstColNames.append('nTotalNotTruncated')
        lstColNames.append('nTotalNullContributors')
        lstColNames.append('nTotalNotNullContributors')
        lstColNames.append('nTotalPossibleSensitive')
        lstColNames.append('nTotalNotPossibleSensitive')
        lstColNames.append('nTotalNullGeo')
        lstColNames.append('nTotalNotNullGeo')
        lstColNames.append('nTotalNullPlace')
        lstColNames.append('nTotalNotNullPlace')
        ##########################################
        for i in range(MAX_LOC_COLS_NUM):
            lstColNames.append('TopLoc%2d' % (i+1))
        #Url, image, video in tweets        
        lstColNames.append('nRatioUrlInTweets')
        lstColNames.append('nTotalUrlInTweets')    
        lstColNames.append('nRatioImageInTweets')
        lstColNames.append('nTotalImageInTweets')
        lstColNames.append('nRatioVideoInTweets')
        lstColNames.append('nTotalVideoInTweets')
        lstColNames.append('nRatioSymbolInTweets')
        lstColNames.append('nTotalSymbolInTweets')
        #language of tweets
        lstColNames.append('nTotalLang')

        for i in range(MAX_LANG_COLS_NUM):
            lstColNames.append('TopLanguage%2d' % (i+1))
        #Tweets frequency
        for key in self.arrTweetTimeFrequency:
            lstColNames.append('TweetTime%2d-%2d' % (key*4+1, key*4+4))
        for key in self.arrTweetDayFrequency:
            lstColNames.append('TweetDay%2d' % (key))
        for key in self.arrTweetWeekFrequency:
            lstColNames.append('TweetWeek%2d' % (key))
        for key in self.arrTweetMonthFrequency:
            lstColNames.append('TweetMonth%2d' % (key))
        #Retweets frequency
        for key in self.arrRetweetTimeFrequency:
            lstColNames.append('RetweetTime%2d-%2d' % (key*4+1, key*4+4))
        for key in self.arrRetweetDayFrequency:
            lstColNames.append('RetweetDay%2d' % (key))
        for key in self.arrRetweetWeekFrequency:
            lstColNames.append('RetweetWeek%2d' % (key))
        for key in self.arrRetweetMonthFrequency:
            lstColNames.append('RetweetMonth%2d' % (key))
        #Source Tweet time frequency
        for key in self.arrTweetFBTimeFrequency:
            lstColNames.append('FBTweetTime%2d' % (key))
        for key in self.arrTweetAndroidTimeFrequency:
            lstColNames.append('AndroidTweetTime%2d' % (key))
        for key in self.arrTweetIphoneTimeFrequency:
            lstColNames.append('IphoneTweetTime%2d' % (key))
        for key in self.arrTweetOtherTimeFrequency:
            lstColNames.append('OtherTweetTime%2d' % (key))
        #Mentioned users
        lstColNames.append('nTotalMentionedUsers')
        #print('%d' % self.arrMentionedUsers)
        for i in range(MAX_USERS_COLS_NUM):
            lstColNames.append('TopMentionedUsers%2d' % (i+1))
        #Hashtags
        lstColNames.append('nTotalHastags')
        #print('%d' % self.arrTopHastags)        
        for i in range(MAX_HASHTAGS_COLS_NUM):
            lstColNames.append('TopHashtags%2d' % (i+1))
        #Trending topics
        lstColNames.append('nTotalInTrending')
        #writer = io.StringIO()
        #return writer.getvalue()
        return lstColNames
    
    def getSentimentNLTK(self, tweetSentence):
        score = []
        print('==============getSentimentNLTK starts ====================')
        #print(tweetSentence)
        sid = SentimentIntensityAnalyzer()
        sentimentScore = sid.polarity_scores(tweetSentence)
        score.append(sentimentScore['neu']) 
        score.append(sentimentScore['neg']) 
        score.append(sentimentScore['pos']) 
        score.append(sentimentScore['compound']) 
        print(tweetSentence)
        print('score = ',score)
        print('==============getSentimentNLTK ends ====================')

    
    
    
    
    def exportCSV(self, bIncludeUserId, userid, bIncludeScreenName, screen_name):
        #writer = io.StringIO()
        lstItems = []
        if(bIncludeUserId):
            lstItems.append(userid)
        if(bIncludeScreenName):
            lstItems.append(screen_name)        
        lstItems.append(self.nTotalTweets)
        lstItems.append(self.nTotalRetweets)
        lstItems.append(self.nTotalQuoteStatus)
        lstItems.append(self.nTotalMentionedTweets)
        lstItems.append(self.nTotalMentionedRetweets)
        lstItems.append(self.nTotalInReplyTweets)
        lstItems.append(self.nTotalFavoritedTweets)
        lstItems.append(self.nTotalFavorites)
        lstItems.append(self.nTotalNullCoordinates)
        lstItems.append(self.nTotalNotNullCoordinates)
        lstItems.append(self.nTotalTruncated)
        lstItems.append(self.nTotalNotTruncated)
        lstItems.append(self.nTotalNullContributors)
        lstItems.append(self.nTotalNotNullContributors)
        lstItems.append(self.nTotalPossibleSensitive)
        lstItems.append(self.nTotalNotPossibleSensitive)
        lstItems.append(self.nTotalNullGeo)
        lstItems.append(self.nTotalNotNullGeo)
        lstItems.append(self.nTotalNullPlace)
        lstItems.append(self.nTotalNotNullPlace)
        ##########################################
        self.exportArrToDelim(self.arrTopLocation, lstItems, True, MAX_LOC_COLS_NUM, 0)     
        lstItems.append(self.nRatioUrlInTweets)
        lstItems.append(self.nTotalUrlInTweets)    
        lstItems.append(self.nRatioImageInTweets)
        lstItems.append(self.nTotalImageInTweets)
        lstItems.append(self.nRatioVideoInTweets)
        lstItems.append(self.nTotalVideoInTweets)
        lstItems.append(self.nRatioSymbolInTweets)
        lstItems.append(self.nTotalSymbolInTweets)
        #language of tweets
        lstItems.append(self.nTotalLang)
        #lstItems.append(self.arrTopLang)
        self.exportArrToDelim(self.arrTopLang, lstItems, True, MAX_LANG_COLS_NUM, 0)
        print('User %s: NoStatsCols after add langs=%d' % (screen_name, len(lstItems)))
        #Tweets frequency
        for key in self.arrTweetTimeFrequency:
            lstItems.append((self.arrTweetTimeFrequency[key]))
        for key in self.arrTweetDayFrequency:
            lstItems.append((self.arrTweetDayFrequency[key]))
        for key in self.arrTweetWeekFrequency:
            lstItems.append((self.arrTweetWeekFrequency[key]))
        for key in self.arrTweetMonthFrequency:
            lstItems.append((self.arrTweetMonthFrequency[key]))
        print('User %s: NoStatsCols after add Tweets frequency=%d' % (screen_name, len(lstItems)))
        #Retweets frequency
        for key in self.arrRetweetTimeFrequency:
            lstItems.append((self.arrRetweetTimeFrequency[key]))
        for key in self.arrRetweetDayFrequency:
            lstItems.append((self.arrRetweetDayFrequency[key]))
        for key in self.arrRetweetWeekFrequency:
            lstItems.append((self.arrRetweetWeekFrequency[key]))
        for key in self.arrRetweetMonthFrequency:
            lstItems.append((self.arrRetweetMonthFrequency[key]))
        print('User %s: NoStatsCols after add Retweets frequency=%d' % (screen_name, len(lstItems)))
        #Source Tweet time frequency
        for key in self.arrTweetFBTimeFrequency:
            lstItems.append((self.arrTweetFBTimeFrequency[key]))
        for key in self.arrTweetAndroidTimeFrequency:
            lstItems.append((self.arrTweetAndroidTimeFrequency[key]))
        for key in self.arrTweetIphoneTimeFrequency:
            lstItems.append((self.arrTweetIphoneTimeFrequency[key]))
        for key in self.arrTweetOtherTimeFrequency:
            lstItems.append((self.arrTweetOtherTimeFrequency[key]))
        #Mentioned users
        print('User %s: NoStatsCols after add src time frequency=%d' % (screen_name, len(lstItems)))
        lstItems.append(self.nTotalMentionedUsers)
        #print(self.arrMentionedUsers)
        self.exportArrToDelim(self.arrMentionedUsers, lstItems, True, MAX_USERS_COLS_NUM, 0)
        #print('User %s: NoStatsCols after add users=%d' % (screen_name, len(lstItems)))
        #Hashtags
        lstItems.append(self.nTotalHastags)
        #print(self.arrTopHastags)
        self.exportArrToDelim(self.arrTopHastags, lstItems, True, MAX_HASHTAGS_COLS_NUM, 0)
        #print('User %s: NoStatsCols after add hashtags=%d' % (screen_name, len(lstItems)))
        #Trending topics
        lstItems.append(self.nTotalInTrending)
        #return writer.getvalue()
        return lstItems
    
def performUserTweetStatsTest():
    screen_name = "ylecun"
    userTweetsStatsAnalyzer = UserTweetStats(screen_name)
    allJsonTweets = userTweetsStatsAnalyzer.loadAllJsonTweets('%s_tweets.json' % screen_name)
    userTweetsStatsAnalyzer.analyze(allJsonTweets)   
    userTweetsStatsAnalyzer.print()
    userStatsColNames = userTweetsStatsAnalyzer.getFeaturesNames(True, True)
    userStatsStr = userTweetsStatsAnalyzer.exportCSV(True, 123456789, True, screen_name)
    print(userStatsColNames)
    print(userStatsStr)

def performUserProfileTest():
    userProf = UserProfile()
    userProf.readScreenNameList('1.csv')
    lstUserStats = []
    for screen_name in userProf.screenNameList:
        #analyze user profile
        userProf.analyzeUserProfile(screen_name)
        #analyze user tweet stats
        userTweetsStatsAnalyzer = UserTweetStats(screen_name)
        if(not os.path.isfile('%s_tweets.json' % screen_name)):
            userTweetsStatsAnalyzer.get_all_tweets(screen_name)
        allJsonTweets = userTweetsStatsAnalyzer.loadAllJsonTweets('%s_tweets.json' % screen_name)
        userTweetsStatsAnalyzer.analyze(allJsonTweets)
        userStatsStr = userTweetsStatsAnalyzer.exportCSV(False, 123456789, False, screen_name)
        print('User %s: number of stats cols=%d' % (screen_name, len(userStatsStr)))
        lstUserStats.append(userStatsStr)
    userStatsColNames = userTweetsStatsAnalyzer.getFeaturesNames(False, False)
    print('Number of stats column names=%d' % (len(userStatsColNames)))
    userProf.exportCSV('userAlls.csv', userStatsColNames, lstUserStats)
    
performUserTweetStatsTest()
