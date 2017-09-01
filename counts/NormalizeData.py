
# coding: utf-8

# In[2]:

import numpy as np 
import pandas as pd
from sklearn import preprocessing

#### Input file will be row wised normalized


class NormalizeHashTagCount:
    def doNormalizarion(self,filePath):
        normal = list()
        hashtags = list()
        df = pd.read_csv(filePath, index_col=0)
        
        #df_matrix = df.as_matrix()
        #df_matrix = df_matrix[:,1:]
        
        
        df_norm = preprocessing.normalize(df, axis = 1)
        df_norm = pd.DataFrame(df_norm, index=df.index.tolist(), columns=df.columns.tolist())
        df_norm.to_csv('C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\result_hourly_matrix\\Hashtag_Count_Hourly_IndirectInfluence_Normalized.csv')
        
        
    
filePath = "C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\result_hourly_matrix\\Hashtag_Count_Hourly_IndirectInfluence.csv"
notmalize = NormalizeHashTagCount()  
notmalize.doNormalizarion(filePath)




# In[ ]:



