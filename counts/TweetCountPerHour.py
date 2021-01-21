import pandas as pd
import os
from sklearn import preprocessing

class TweetCountPerDay:
    
    def getDateWiseCount(self):
        cur_dir = '..\\twitter_bot\\twitter_data\\parsed\\temp\\'
        out_dir = '..\\twitter_bot\\twitter_data\\parsed\\'
        dirs = os.listdir(cur_dir)
        outputFile = out_dir+'result_tweet_fileMoreThan10000.csv'
        for file in dirs:
            filePath = cur_dir+file
            
            data = pd.read_csv(filePath)
            df = pd.DataFrame(data)
            df1 = df
            #print(data)
            df_date = df[['created_at_list']]
            print(df_date)
            
tweetcount = TweetCountPerDay()
tweetcount.getDateWiseCount()