import pandas as pd
import csv
import json
import re
import sys
import os
import tweepy


########################################################################################################
############ I/P : Folder path having files, parsed by TweetParserBasedOnHashTags.py####################
############ O/P : This progam creates out file containing every user with their in/directinfluence ####
########################################################################################################




class InfuenceCount:
    def __init__(self):    
        self.created_day_list = list()
        self.created_date_list = list()
        self.created_month_list = list()
        self.created_year_list = list()
        self.created_hour_list = list()
        self.created_min_list = list()
        self.created_sec_list = list()
        self.directinfluence_list = list()
        self.indirectinfluence_list = list()
        
        self.tweetID_list = list()
        self.screenName_list = list()
        self.mention_list = list()
        #self.mention_list.append("Mention List")
        self.userfollower_list = list()
        self.mentionfollower_list = list()
        #self.mentionfollower_list.append("Mention Followers")
        
        
        self.id_list = list()
        
        self.mentionDict = dict()
         
    def getDay(self,day):
        dayOfWeek={'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':7}
        return dayOfWeek[day]    
        
    def getMonth(self,month):
        monthToNumber={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return monthToNumber[month]
    
    def countMentions(self, text):
        afterSplit = text.split('@')
        #print(afterSplit)
        afterSplit = {}
        numberOfMentions = len(afterSplit)
        return numberOfMentions           
    
    def findInfluence(self,filePath,file):
        CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXX'
        CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        df = pd.read_csv(filePath)
        
        df_influence = df[["id_list","created_at_list","screen_name_list","followers_count_list"]]
        text = df[["text_list"]]
        textList = text.values.tolist()
        for i in range(len(textList)):
            tempText = textList[i]
            #print(tempText[0])
            atTheRate = '@'
            totalFollower = 0
            follower = 0
            if atTheRate in tempText[0]:
                pattern = r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)'
                pattern=re.compile(pattern)
                tempText  = pattern.findall(str(tempText))
                self.mention_list.append(tempText)
                print(tempText)
                if (len(tempText) > 0):
                    
                    for i in range(len(tempText)):
                        mentionLocal = tempText[i]

                        if mentionLocal in self.mentionDict:
                            follower = self.mentionDict[mentionLocal]
                            totalFollower = totalFollower + follower
                            #print()
                        else:
                            try:
                                user = api.get_user(mentionLocal)
                                follower = user.followers_count
                                print('')
                            except:
                                follower = 0
                            self.mentionDict[mentionLocal] = follower
                            totalFollower = totalFollower + follower
                self.mentionfollower_list.append(totalFollower)
                
            else:
                self.mention_list.append("")
                self.mentionfollower_list.append(0)    
                    
       
        
        out = {'Mention List':self.mention_list, 'Mention Followers List':self.mentionfollower_list}
        df_ = pd.DataFrame(out)
        result = [df_influence, df_]
        result = pd.concat(result, axis=1)
        result.to_csv("\\influence\\trung\\"+fileNameWithOutType+".csv")
       
        
        
        
        
           
                    
                
                
                
    
path = '\\parsed\\New folder\\'
dirs = os.listdir( path )
#print(dirs)
for file in dirs:
    filePath = path+file 
    print(filePath)
    influence = InfuenceCount()  
    influence.findInfluence(filePath,file)

