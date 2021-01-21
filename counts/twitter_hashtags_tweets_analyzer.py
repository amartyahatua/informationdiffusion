'''
Created on Jul 25, 2017

@author: tnguyen
'''
from __future__ import absolute_import, print_function

import csv
import json
import datetime
from datetime import datetime
from email.utils import parsedate
from collections import defaultdict
import io
import os
import operator
import re
import sys
import os.path
import time

class HashtagsTweetObject(object):
    def __init__(self):
        self.id = 0
        self.id_str = ''
        self.user_id = ''
        self.user_screen_name = ''
        self.user_created_at = ''
        self.user_favorites_count = 0
        self.user_listed_count = 0
        self.user_statuses_count = 0
        self.user_followers_count = 0
        self.user_friends_count = 0
        self.text = ''
        self.source = ''
        self.created_at = ''
        self.lang = ''
        self.geo = ''
        self.place = ''
        self.entities_symbols = []
        self.entities_user_mentions = []
        self.entities_hashtags = []
        self.entities_urls = []
        self.entities_media_image = []
        self.entities_media_video = []
        self.entities_media_other = []
        self.contributors = ''
        self.coordinates = ''        
        self.favorite_count = 0
        self.retweet_count = 0
        self.metadata_result_type = ''
        self.metadata_iso_lang_code = ''
        self.is_quote_status = False
        self.possibly_sensitive = False
        self.truncated = False
        self.favorited = False
        self.retweeted = False
        self.retweeted_status_id = ''
        self.retweeted_status_created_at = ''
        self.retweeted_status_user_screen_name = ''
        self.retweeted_status_retweet_count = 0
        self.in_reply_to_status_id = ''
        self.in_reply_to_screen_name = ''
        self.in_reply_to_status_id_str = ''
        self.in_reply_to_user_id = ''
        self.in_reply_to_user_id_str = ''
        
    def getColumnNamesList(self):
        lstColNames = []
        lstColNames.append('id')
        lstColNames.append('id_str')
        lstColNames.append('user_id')
        lstColNames.append('user_screen_name')
        lstColNames.append('user_created_at')
        lstColNames.append('text')
        lstColNames.append('source')
        lstColNames.append('created_at')
        lstColNames.append('lang')
        lstColNames.append('geo')
        lstColNames.append('place')
        lstColNames.append('entities_symbols')
        lstColNames.append('entities_user_mentions')
        lstColNames.append('entities_hashtags')
        lstColNames.append('entities_urls')
        lstColNames.append('entities_media_image')
        lstColNames.append('entities_media_video')
        lstColNames.append('entities_media_other')
        lstColNames.append('contributors')
        lstColNames.append('coordinates')        
        lstColNames.append('favorite_count')
        lstColNames.append('retweet_count')
        lstColNames.append('metadata_result_type')
        lstColNames.append('metadata_iso_lang_code')
        lstColNames.append('is_quote_status')
        lstColNames.append('possibly_sensitive')
        lstColNames.append('truncated')
        lstColNames.append('favorited')
        lstColNames.append('retweeted')
        lstColNames.append('retweeted_status_id')
        lstColNames.append('retweeted_status_created_at')
        lstColNames.append('retweeted_status_user_screen_name')
        lstColNames.append('retweeted_status_retweet_count')
        lstColNames.append('in_reply_to_status_id')
        lstColNames.append('in_reply_to_screen_name')
        lstColNames.append('in_reply_to_status_id_str')
        lstColNames.append('in_reply_to_user_id')
        lstColNames.append('in_reply_to_user_id_str')
        return lstColNames
    
    def getItemsList(self):
        lstItems = []
        lstItems.append(self.id)
        lstItems.append(self.id_str)
        lstItems.append(self.user_id)
        lstItems.append(self.user_screen_name)
        lstItems.append(self.user_created_at)
        lstItems.append(self.text)
        lstItems.append(self.source)
        lstItems.append(self.created_at)
        lstItems.append(self.lang)
        lstItems.append(self.geo)
        lstItems.append(self.place)
        lstItems.append(self.entities_symbols)
        lstItems.append(self.entities_user_mentions)
        lstItems.append(self.entities_hashtags)
        lstItems.append(self.entities_urls)
        lstItems.append(self.entities_media_image)
        lstItems.append(self.entities_media_video)
        lstItems.append(self.entities_media_other)
        lstItems.append(self.contributors)
        lstItems.append(self.coordinates)
        lstItems.append(self.favorite_count)
        lstItems.append(self.retweet_count)
        lstItems.append(self.metadata_result_type)
        lstItems.append(self.metadata_iso_lang_code)
        lstItems.append(self.is_quote_status)
        lstItems.append(self.possibly_sensitive)
        lstItems.append(self.truncated)
        lstItems.append(self.favorited)
        lstItems.append(self.retweeted)
        lstItems.append(self.retweeted_status_id)
        lstItems.append(self.retweeted_status_created_at)
        lstItems.append(self.retweeted_status_user_screen_name)
        lstItems.append(self.retweeted_status_retweet_count)
        lstItems.append(self.in_reply_to_status_id)
        lstItems.append(self.in_reply_to_screen_name)
        lstItems.append(self.in_reply_to_status_id_str)
        lstItems.append(self.in_reply_to_user_id)
        lstItems.append(self.in_reply_to_user_id_str)
        return lstItems

class HashtagsTweetsAnalyzer(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        #self.listHashtags = []
        self.dictHourCnt = defaultdict(int)
        self.nTotalTweets = 0
        self.listTweetObjs = []
        self.hashtag = ''
    
    def  readHashtagsList(self, fileName):
        
        listHashtags = []
        with open(fileName) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                listHashtags.append(row[0])
        return listHashtags
    
    def loadAllJsonTweets(self, fileName):
        with open(fileName) as data_file:    
            data = json.load(data_file) 
        return data
    
    def analyzeUserTweetTime(self, tweet):
        hourIdx = -1
        if(tweet['created_at'] is not None):
            #print(tweet['created_at'])
            created_at = datetime(*(parsedate(tweet['created_at'])[:6]))
            hourIdx = created_at.year * 1000000 + created_at.month * 10000 + created_at.day * 100 + created_at.hour
        return hourIdx
    
    def analyze(self, alltweets):
        for tweet in alltweets:
            # count tweet based on hourly rate
            hourIdx = self.analyzeUserTweetTime(tweet)
            self.dictHourCnt[hourIdx] += 1
            # analyze other properties to export to csv
            tweetObj = HashtagsTweetObject()
            tweetObj.id = tweet['id']
            tweetObj.id_str = tweet['id_str']
            tweetObj.user_id = tweet['user']['id']
            tweetObj.user_screen_name = tweet['user']['screen_name']
            tweetObj.user_created_at = tweet['user']['created_at']
            tweetObj.text = tweet['text'].encode('utf-8')
            tweetObj.source = tweet['source']
            tweetObj.created_at = tweet['created_at']
            if(tweet['lang'] is not None):
                tweetObj.lang = tweet['lang']
            if(tweet['geo'] is not None):
                tweetObj.geo = tweet['geo']
            if(tweet['place'] is not None):
                tweetObj.place = tweet['place']
            if(tweet['contributors'] is not None):
                tweetObj.contributors = tweet['contributors']
            if(tweet['coordinates'] is not None):
                tweetObj.coordinates = tweet['coordinates']
            tweetObj.favorite_count = tweet['favorite_count']
            tweetObj.retweet_count = tweet['retweet_count']
            if(tweet['metadata'] is not None):
                tweetObj.metadata_result_type = tweet['metadata']['result_type']
                tweetObj.metadata_iso_lang_code = tweet['metadata']['iso_language_code']
            tweetObj.is_quote_status = tweet['is_quote_status']
            if(tweet.get('possibly_sensitive', '') != ''):
                tweetObj.possibly_sensitive = tweet['possibly_sensitive']
            if(tweet.get('truncated', '') != ''):
                tweetObj.truncated = tweet['truncated']
            if(tweet.get('favorited', '') != ''):
                tweetObj.favorited = tweet['favorited']
            if(tweet['retweeted'] is not None):
                tweetObj.retweeted = tweet['retweeted']
            if(tweet.get('retweeted_status', 'null') != 'null'):                
                tweetObj.retweeted_status_id = tweet['retweeted_status']['id']
                tweetObj.retweeted_status_created_at = tweet['retweeted_status']['created_at']
                tweetObj.retweeted_status_user_screen_name = tweet['retweeted_status']['user']['screen_name']
                tweetObj.retweeted_status_retweet_count = tweet['retweeted_status']['retweet_count']
            if(tweet['in_reply_to_status_id'] is not None):
                tweetObj.in_reply_to_status_id = tweet['in_reply_to_status_id']
            if(tweet['in_reply_to_screen_name'] is not None):
                tweetObj.in_reply_to_screen_name = tweet['in_reply_to_screen_name']
            if(tweet['in_reply_to_status_id_str'] is not None):
                tweetObj.in_reply_to_status_id_str = tweet['in_reply_to_status_id_str']
            if(tweet['in_reply_to_user_id'] is not None):
                tweetObj.in_reply_to_user_id = tweet['in_reply_to_user_id']
            if(tweet['in_reply_to_user_id_str'] is not None):
                tweetObj.in_reply_to_user_id_str = tweet['in_reply_to_user_id_str']
            #analyze entities
            entities = tweet['entities']
            if(len(entities['symbols']) > 0):
                for symbol in entities['symbols']:
                    tweetObj.entities_symbols.append(symbol['text'])

            lstMentionedUsers = entities.get('user_mentions',[])
            for mentioned_user in lstMentionedUsers:            
                tweetObj.entities_user_mentions.append(mentioned_user['screen_name'])

            if(len(entities['hashtags']) > 0):                
                for hash_tags in entities['hashtags']:
                    tweetObj.entities_hashtags.append(hash_tags['text'])
            if(len(entities['urls']) > 0):
                for url in entities['urls']:
                    tweetObj.entities_urls.append(url['expanded_url'])

            lstMedia = entities.get('media', [])    
            if(len(lstMedia) > 0):
                for media_element in lstMedia:
                    if(media_element['type'] == 'photo'):
                        tweetObj.entities_media_image.append(media_element['media_url'])
                    elif (media_element['type'] == 'video'):
                        tweetObj.entities_media_video.append(media_element['media_url'])
                    else:
                        tweetObj.entities_media_other.append(media_element['media_url'])

            self.listTweetObjs.append(tweetObj)
        
    def exportTweetsJsonToCSV(self, outFileName):
        with open(outFileName,'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
            bWriteHeader = False
            for tweetObj in self.listTweetObjs:
                if(bWriteHeader == False):
                    lstColNames = tweetObj.getColumnNamesList()
                    writer.writerow(lstColNames)
                    bWriteHeader = True
                lstItems = tweetObj.getItemsList()
                writer.writerow(lstItems)
            csvfile.close()

def testHashtagsAnalyzer(jsonFileName):
    analyzer = HashtagsTweetsAnalyzer()
    alltweets = analyzer.loadAllJsonTweets(jsonFileName)
    analyzer.analyze(alltweets)
    print(analyzer.dictHourCnt)
    analyzer.exportTweetsJsonToCSV(jsonFileName.replace('.json', '.csv'))

def performHashtagsAnalysisAndExporting(hashtagsFolder, csvOutputFolder):
    lstHTAnalyzeResults = []
    lstHourKeys = []
    cnt = 0
    for file in os.listdir(hashtagsFolder):
        if file.endswith(".json"):
            cnt += 1
            fullFilePath = os.path.join(hashtagsFolder, file) 
            print(fullFilePath)
            analyzer = HashtagsTweetsAnalyzer()
            alltweets = analyzer.loadAllJsonTweets(fullFilePath)
            analyzer.hashtag = file.replace('.json', '')
            analyzer.analyze(alltweets)
            print(analyzer.dictHourCnt)
            for key in analyzer.dictHourCnt:
                if(key not in lstHourKeys):
                    lstHourKeys.append(key)
            #output csv formatted file
            outputFilePath = os.path.join(csvOutputFolder, file) 
            analyzer.exportTweetsJsonToCSV(outputFilePath.replace('.json', '.csv'))
            #add to list
            lstHTAnalyzeResults.append(analyzer)
            alltweets.clear()

    lstHourKeys.sort()
    lstColNames = []
    lstColNames.append('Hashtag')
    for key in lstHourKeys:
        lstColNames.append(key)
    #write csv file 
    with open('Hashtag_Hourly_Count.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
        #write headers first
        writer.writerow(lstColNames)
        #write hashtags count
        lstItems = []
        for analyzer in lstHTAnalyzeResults:
            lstItems.clear()
            lstItems.append(analyzer.hashtag)
            for key in lstHourKeys:
                if(key in analyzer.dictHourCnt):
                    lstItems.append(analyzer.dictHourCnt[key])
                else:
                    lstItems.append(0)
            writer.writerow(lstItems)
        csvfile.close()
    return True


performHashtagsAnalysisAndExporting('./Hashtags', './Hashtags_csv')