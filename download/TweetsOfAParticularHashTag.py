import tweepy
import json
CONSUMER_KEY = '******************'
CONSUMER_SECRET = '*********************************************'
ACCESS_KEY = '*********************************************'
ACCESS_SECRET = '*********************************************'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

import csv


########################################################################################################
########## I/P : The input file contains list of HashTags in hashtags_part2.csv. We want to downloaded##
#################    tweets of that particular HashTag  ################################################
############ O/P : .json file corresponds to each HashTag containing the tweets ########################
########################################################################################################




with open('...\\hashtags_part2.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        nTweet = 0
        #flag = 1
        with open('...\\tweets\\'+row[0]+'.json', 'w') as outfile:
            outfile.write('[')
            for page in tweepy.Cursor(api.search, q='#'+row[0], count=1000).pages():

                for tweet in page:
                    nTweet = nTweet + 1
                    if(nTweet > 1):
                        outfile.write(',')
                    outfile.write(json.dumps(tweet._json))

                if(nTweet >= 100000):   #### 100000 is the maximum tweets can be downloaded using this code. To change the limit change the number
                    break
            print(row[0], ' => ', nTweet, ' tweets downloaded')
            outfile.write(']')