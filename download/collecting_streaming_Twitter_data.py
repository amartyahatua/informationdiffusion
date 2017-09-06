from __future__ import absolute_import, print_function

import csv
import datetime
import json
import time
import os
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitter import parse_data
############################################################################
#############This file collect Twitter streaming data and stores with ######
######file name as per the date and time. The time limit is 5 minutes#######
############################################################################

class collect_data:
    
    
        

    consumer_key="Ig8MZcPR3UP4v2qz14DSqSLAb"
    consumer_secret="w1LvOKk7CKX9VvRCBhaYNQwQf7LJvuNddVG7h5QMqZ8NLD5QgI"
     
    # After the step above, you will be redirected to your app's page.
    # Create an access token under the the "Your access token" section
    access_token="813832637383053318-iCrCeji9udZQNbZyiITiX7YSQ469xrL"
    access_token_secret="3ev1HrT17JH5Xii9RzLpkk7Xw7gLMP67JpT18WJa6fbUn"
    
    
    class MyListener(StreamListener):    
        def __init__(self, time_limit=600, max_tweets=9999, fileName='stream.json'):
            self.start_time = time.time()
            self.limit = time_limit
            self.tweet_number=0   # class variable
            self.max_tweets = max_tweets
            self.saveFile = open(fileName, 'a')
            self.saveFile.write('[')
            super(StreamListener, self).__init__()
        def on_data(self, data):
            self.tweet_number = self.tweet_number + 1
            if (time.time() - self.start_time) < self.limit and self.tweet_number < self.max_tweets:
                if self.tweet_number >1 : 
                    self.saveFile.write(',')
                try: 
                    self.saveFile.write(data)
                except :
                    print('error')
                #self.saveFile.write('\n')
                return True
            else:
                self.saveFile.write(']')
                self.saveFile.close()
                return False
        def on_error(self, status):
            print(status)
    run = 'start'
    
    
    
    if run == "start":
        for i in range(2): 
            directory = 'Z:\\raw\\Day-'+str(i)+'\\'
            os.makedirs(directory)
            mins = 0
            while mins != 288:    
                ## File name 
                time_date = str(datetime.datetime.now())
                time_date = time_date[:10]+'_'+time_date[11:13]+'_'+time_date[14:16]
                file_name = directory
                file_name = file_name +  str(time_date)
                file_name = file_name + '.json'
                 
                ## Get streaming data
                l = MyListener(time_limit=300, fileName=file_name)
                auth = OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                stream = Stream(auth, l)
                stream.sample()
                time.sleep(20)
                mins += 1
                print(file_name)
                #parse_data.doParsing(1,file_name)
                



