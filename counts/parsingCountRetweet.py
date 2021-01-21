
# coding: utf-8

# In[ ]:

import csv
import json
import re
import sys
import os


from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
#from sentiment import Sentiment
#from topicModeling2_wiki  import TopicModeling
#from geopy.geocoders import Nominatim

class TweetParserBasedOnHashTagsRetweet:
    def __init__(self):  
		self.formatedDate_list = list()
        self.formatedMonth_list = list()
        self.formatedYear_list = list()
        self.formatedHour_list = list()
        self.newformatedDate_list = list()


		

        
        
        
        
        
    
    

    
    
    
    
    def doParsing(self,fileName,file):
	
		fileNameWithOutType = file.split(".")[0]
        parsed_file = "..\\twitter_bot\\twitter_data\\parsed\\hour_retweet_trung"+fileNameWithOutType+".csv"
		
		data = pd.read_csv(fileName)
		df = pd.DataFrame(data)
		
		df_date = df[['created_at_list']]
		df_date = df_date.values.tolist()
		remove_ms = lambda x:re.sub("\+\d+\s","",x)

		# Make the string into a datetime object.
		mk_dt = lambda x:datetime.strptime(remove_ms(x), "%a %b %d %H:%M:%S %Y")

		# Format your datetime object.
		my_form_D = lambda x:"{:%d}".format(mk_dt(x))
		my_form_M = lambda x:"{:%m}".format(mk_dt(x))
		my_form_Y = lambda x:"{:%Y}".format(mk_dt(x))
		my_form_H = lambda x:"{:%H}".format(mk_dt(x))
		
		for i in range(len(df_date)):
			newFormat = my_form_D(str(df_date[i][0]))
			self.formatedDate_list.append(newFormat)
			
			newFormat = my_form_M(str(df_date[i][0]))
			self.formatedMonth_list.append(newFormat)
			
			newFormat = my_form_Y(str(df_date[i][0]))
			self.formatedYear_list.append(newFormat)
			
			newFormat = my_form_H(str(df_date[i][0]))
			self.formatedHour_list.append(newFormat)
		
		
		
		
		
		
		
		
		
		
   
                                             
        
path = '..\\twitter_bot\\twitter_data\\parsed\\Hashtags_csv\\'
dirs = os.listdir( path )
#print(dirs)
for file in dirs:
    fileName = path+file 
    print(fileName)
    parsing = TweetParserBasedOnHashTagsRetweet()
    parsing.doParsing(fileName,file)
