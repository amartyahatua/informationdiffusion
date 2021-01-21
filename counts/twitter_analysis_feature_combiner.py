'''
Created on Aug 7, 2017

@author: Trung
'''
import csv
import numpy
import os.path
import pandas as pd
#import datetime
from datetime import datetime
from collections import defaultdict
from email.utils import parsedate

def exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTAnalyzeResults, csvOutputFolder, outputFileName):
    #sort keys
    lstHourKeys.sort()
    lstColNames = []
    lstColNames.append('Hashtag')
    for key in lstHourKeys:
        lstColNames.append(key)
    #write csv file 
    outFullFilePath = os.path.join(csvOutputFolder, outputFileName) 
    with open(outFullFilePath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
        #write headers first
        writer.writerow(lstColNames)
        #write hashtags count
        lstItems = []
        for hashtag, dictCnt in lstHTAnalyzeResults.items():
            lstItems.clear()
            lstItems.append(hashtag)
            for key in lstHourKeys:
                if(key in dictCnt):
                    lstItems.append(dictCnt[key])
                else:
                    lstItems.append(0)
            writer.writerow(lstItems)
        csvfile.close()

def performCombineTwitterVolumeFeatures(listHashtagsFolder, bHasIndexColumn, csvOutputFolder, outputFileName):
    lstHTAnalyzeResults = {}
    lstHourKeys = []
    cnt = 0
    for folder in listHashtagsFolder:
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                cnt += 1
                hashtag = os.path.splitext(file)[0]
                fullFilePath = os.path.join(folder, file) 
                print(fullFilePath)
                if(bHasIndexColumn):
                    df = pd.read_csv(fullFilePath, index_col=0)
                else:
                    df = pd.read_csv(fullFilePath)
                dictHourCnt = defaultdict(int)
                for index, row in df.iterrows():
                    hourIdx = row['formatedYear_list'] * 1000000 +  row['formatedMonth_list'] * 10000 \
                        + row['formatedDate_list'] * 100 + row['formatedHour_list']
                    dictHourCnt[hourIdx] += 1
                for key in dictHourCnt:
                    if(key not in lstHourKeys):
                        lstHourKeys.append(key)
                lstHTAnalyzeResults[hashtag] = dictHourCnt

    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTAnalyzeResults, csvOutputFolder, outputFileName)
        

def performCombineTwitterSentimentFeatures(listHashtagsFolder, bHasIndexColumn, csvOutputFolder, outputFileName):
    lstHTPosPercentageResults = {}
    lstHTNeuPercentageResults = {}
    lstHTNegPercentageResults = {}
    lstHTPosScoreResults = {}
    lstHTNeuScoreResults = {}
    lstHTNegScoreResults = {}
    lstHourKeys = []
    cnt = 0
    for folder in listHashtagsFolder:
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                cnt += 1
                hashtag = os.path.splitext(file)[0]
                fullFilePath = os.path.join(folder, file) 
                print(fullFilePath)
                if(bHasIndexColumn):
                    df = pd.read_csv(fullFilePath, index_col=0)
                else:
                    df = pd.read_csv(fullFilePath)
                dictHourTweetCnt = defaultdict(int)
                dictHourPosCnt = defaultdict(float)
                dictHourNeuCnt = defaultdict(float)
                dictHourNegCnt = defaultdict(float)
                dictHourPosScore = defaultdict(float)
                dictHourNeuScore = defaultdict(float)
                dictHourNegScore = defaultdict(float)
                for index, row in df.iterrows():
                    #print(tweet['created_at'])
                    created_at = datetime(*(parsedate(row['created_at_list'])[:6]))
                    hourIdx = created_at.year * 1000000 + created_at.month * 10000 + created_at.day * 100 + created_at.hour
                    dictHourTweetCnt[hourIdx] += 1
                    if(row['negetive'] > row['neutral']):
                        if((row['negetive'] > row['positive'])):
                            dictHourNegCnt[hourIdx] += 1
                            dictHourNegScore[hourIdx] += row['negetive']
                        else:
                            dictHourPosCnt[hourIdx] += 1
                            dictHourPosScore[hourIdx] += row['positive']
                    else:
                        if((row['neutral'] > row['positive'])):
                            dictHourNeuCnt[hourIdx] += 1
                            dictHourNeuScore[hourIdx] += row['neutral']
                        else:
                            dictHourPosCnt[hourIdx] += 1
                            dictHourPosScore[hourIdx] += row['positive']
                for key in dictHourNegScore:
                    dictHourNegCnt[key] = dictHourNegCnt[key] / dictHourTweetCnt[key]
                    dictHourNegScore[key] = dictHourNegScore[key] / dictHourTweetCnt[key]
                for key in dictHourNeuScore:
                    dictHourNeuCnt[key] = dictHourNeuCnt[key] / dictHourTweetCnt[key]
                    dictHourNeuScore[key] = dictHourNeuScore[key] / dictHourTweetCnt[key]
                for key in dictHourPosScore:
                    dictHourPosCnt[key] = dictHourPosCnt[key] / dictHourTweetCnt[key]
                    dictHourPosScore[key] = dictHourPosScore[key] / dictHourTweetCnt[key]
                for key in dictHourTweetCnt:
                    if(key not in lstHourKeys):
                        lstHourKeys.append(key)
                lstHTPosPercentageResults[hashtag] = dictHourPosCnt
                lstHTNeuPercentageResults[hashtag] = dictHourNeuCnt
                lstHTNegPercentageResults[hashtag] = dictHourNegCnt
                lstHTPosScoreResults[hashtag] = dictHourPosScore
                lstHTNeuScoreResults[hashtag] = dictHourNeuScore
                lstHTNegScoreResults[hashtag] = dictHourNegScore
    #export CSV
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTPosPercentageResults, csvOutputFolder, outputFileName+'_PosPercentage.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTNeuPercentageResults, csvOutputFolder, outputFileName+'_NeuPercentage.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTNegPercentageResults, csvOutputFolder, outputFileName+'_NegPercentage.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTPosScoreResults, csvOutputFolder, outputFileName+'_PosScore.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTNeuScoreResults, csvOutputFolder, outputFileName+'_NeuScore.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTNegScoreResults, csvOutputFolder, outputFileName+'_NegScore.csv')

def performCombineTwitterInfluenceFeatures(listHashtagsFolder, bHasIndexColumn, csvOutputFolder, outputFileName):
    lstHTDirectInfluenceResults = {}
    lstHTIndirectInfluenceResults = {}
    lstHourKeys = []
    cnt = 0
    for folder in listHashtagsFolder:
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                cnt += 1
                hashtag = os.path.splitext(file)[0]
                fullFilePath = os.path.join(folder, file) 
                print(fullFilePath)
                if(bHasIndexColumn):
                    df = pd.read_csv(fullFilePath, index_col=0)
                else:
                    df = pd.read_csv(fullFilePath)
                dictHourDirectInfluence = defaultdict(float)
                dictHourIndirectInfluence = defaultdict(float)
                for index, row in df.iterrows():
                    #print(tweet['created_at'])
                    created_at = datetime(*(parsedate(row['created_at_list'])[:6]))
                    hourIdx = created_at.year * 1000000 + created_at.month * 10000 + created_at.day * 100 + created_at.hour
                    #direct influence: user and mentioned users
                    dictHourDirectInfluence[hourIdx] += 1
                    #print(row['Mention List'])
                    if(row['Mention List'] is not numpy.nan and len(str(row['Mention List'])) > 2):
                        mentionedUsers = str(row['Mention List']).replace('[', '')
                        mentionedUsers = mentionedUsers.replace(']', '')
                        mentionedUsers = mentionedUsers.replace('\'', '')
                        mentionedUsers = mentionedUsers.replace('", "', '","')
                        arrUsers = mentionedUsers.split(',')
                        dictHourDirectInfluence[hourIdx] += len(arrUsers)                            
                    #indirect influence => SUM of followers
                    dictHourIndirectInfluence[hourIdx] += row['followers_count_list']
                    dictHourIndirectInfluence[hourIdx] += row['Mention Followers List']
                    if(hourIdx not in lstHourKeys):
                        lstHourKeys.append(hourIdx)
                lstHTDirectInfluenceResults[hashtag] = dictHourDirectInfluence
                lstHTIndirectInfluenceResults[hashtag] = dictHourIndirectInfluence
    #export CSV
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTDirectInfluenceResults, csvOutputFolder, outputFileName+'_DirectInfluence.csv')
    exportTweetTimeSeriesFeaturesToCSV(lstHourKeys, lstHTIndirectInfluenceResults, csvOutputFolder, outputFileName+'_IndirectInfluence.csv')

performCombineTwitterInfluenceFeatures(['./influence_amartya/','./influence_trung/'], True,
                              './', 'Hashtag_Count_Hourly')