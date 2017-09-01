import csv
import json
import re
import sys
import os

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from sentiment import Sentiment
from topicModeling2_wiki  import TopicModeling
from geopy.geocoders import Nominatim


########################################################################################################
########## I/P : .json file of a having Tweets of a particular HashTag #################################
############ O/P : .csv file containing date and time related information of all Tweets ################
########################################################################################################



class TweetsOfAParticularTime:
    def __init__(self):    
        self.created_day_list = list()
        self.created_date_list = list()
        self.created_month_list = list()
        self.created_year_list = list()
        self.created_hour_list = list()
        self.created_min_list = list()
        self.created_sec_list = list()
        self.id_list = list()
        self.lang_list = list()

    def remove_comma(self,text):
        word_search = ','
        result_text = ''
        if word_search in text:
            result_text = text.replace(',', ' ')
        else:
            result_text = text
        return result_text
    
    def remove_b(self,text):
        result_text = ''
        text = str(text)
        if text.startswith('b'):
            result_text = text[1:]
        elif text.startswith('|b'):
            result_text = text[3:]
        else:
            result_text = text
        return result_text
    
    def isEnglish(self,s):
        if re.match("^[A-Za-z0-9_-]*$", s):
            return 1
        else:
            return 0
        
    def getDay(self,day):
        dayOfWeek={'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':7}
        return dayOfWeek[day]    
        
    def getMonth(self,month):
        monthToNumber={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return monthToNumber[month]
    def getLanguage(self,lang):
        lang = lang[0:2]
        languageList = {'en':1,'en-gb':2,'ar':3,'bn':4,'cs':5,'da':6,'de':7,'el':8,'es':9,'fa':10,'fi':11,'fil':12,'fr':13,'he':14,'hi':15,'hu':16,'id':17,'it':18,'ja':19,'ko':20,'msa':21,'nl':22,'no':23,'pl':24,'pt':25,'ro':26,'ru':27,'sv':28,'th':29,'tr':30,'uk':31,'ur':32,'vi':33,'zh-cn':34,'zh-tw':35, 'pt-PT':36, 'zh':37, 'ca':38, 'gl':39, 'sr':40, 'bg':41, 'in':42, 'ms':43}
        return languageList[lang]
    
    def getSourceIndex(self,source):
        sourceList = {"Android":1,"iPhone":2,"Lite":3,"Client":4,"iPad":5,"Inac_Ylna1975":6,"mikoto_EM":7,"twittbot.net":8,"(M2)":9,"Facebook":10,"1.1":11,"Google":12,"Cat":13,"TweetDeck":14,"CabronaMediu":15,"itubot":16,"alexandrumarine1":17,"Instagram":18,"Phone":19,"Post":20,"Buffer":21,"PlacalmoNiarea":22,"RoundTeam":23,"twimaker":24,"CRUISE":25,"Tweetlogix":26,"dlvr.it":27,"skynet_salma32Y":28,"skynet_salma166Y":29,"Incidents":30,"Windows":31,"TweetMyJOBS":32,"WordPress.com":33,"IFTTT":34,"iOS":35,"twicca":36,"SocialOomph":37,"Botize":38}
        try:
            source = sourceList[source]
        except:
            source = 0
        return source
    def getImageType(self,imageType):
        try:
            imageTypeList = {"jpg":1,"png":2,"jpeg":3,"gif":4}
            imageExtns = imageTypeList[imageType]
        except:
            imageExtns = 0
        return imageExtns
    def getTimeZone(self,timezone):
        TimeZoneList = {'Hawaii':36000,'Alaska':32400,'Pacific Time (US & Canada)':28800,'Arizona':25200,'Mountain Time (US &amp; Canada)':25200,
                        'Central Time (US &amp; Canada)':21600,'Eastern Time (US & Canada)':18000,'Indiana (East)':18000,
                        'International Date Line West':39600,'Midway Island':39600,'Samoa':39600,'Tijuana':28800,'Chihuahua':25200,'Mazatlan':25200,
                        'Central America':21600,'Guadalajara':21600,'Mexico City':21600,'Monterrey':21600,'Saskatchewan':21600,'Bogota':18000,
                        'Lima':18000,'Quito':18000,'Caracas':16200,'Atlantic Time (Canada)':14400,'La Paz':14400,'Santiago':14400,'Newfoundland':12600,
                        'Brasilia':10800,'Buenos Aires':10800,'Georgetown':10800,'Greenland':10800,'Mid-Atlantic':7200,'Azores':3600,'Cape Verde Is':3600,
                        'Casablanca':0,'Dublin':0,'Edinburgh':0,'Lisbon':0,'London':0,'Monrovia':0,'Amsterdam':3600,'Belgrade':3600,'Berlin':3600,
                        'Bern':3600,'Bratislava':3600,'Brussels':3600,'Budapest':3600,'Copenhagen':3600,'Ljubljana':3600,'Madrid':3600,'Paris':3600,
                        'Prague':3600,'Rome':3600,'Sarajevo':3600,'Skopje':3600,'Stockholm':3600,'Vienna':3600,'Warsaw':3600,'West Central Africa':3600,
                        'Zagreb':3600,'Athens':7200,'Bucharest':7200,'Cairo':7200,'Harare':7200,'Helsinki':7200,'Istanbul':7200,'Jerusalem':7200,
                        'Kyiv':7200,'Pretoria':7200,'Riga':7200,'Sofia':7200,'Tallinn':7200,'Vilnius':7200,'Baghdad':10800,'Kuwait':10800,'Minsk':10800,
                        'Nairobi':10800,'Riyadh':10800,'Tehran':12600,'Abu':14400,'Baku':14400,'Moscow':14400,'Muscat':14400,'St. Petersburg':14400,
                        'Tbilisi':14400,'Volgograd':14400,'Yerevan':14400,'Kabul':16200,'Islamabad':18000,'Karachi':18000,'Tashkent':18000,
                        'Chennai':19800,'Kolkata':19800,'Mumbai':19800,'New Delhi':19800,'Kathmandu':20700,'Almaty':21600,'Astana':21600,'Dhaka':21600,
                        'Ekaterinburg':21600,'Sri Jayawardenepura':21600,'Rangoon':23400,'Bangkok':25200,'Hanoi':25200,'Jakarta':25200,
                        'Novosibirsk':25200,'Beijing':28800,'Chongqing':28800,'Hong Kong':28800,'Krasnoyarsk':28800,'Kuala Lumpur':28800,'Perth':28800,
                        'Singapore':28800,'Taipei':28800,'Ulaan Bataar':28800,'Urumqi':28800,'Irkutsk':32400,'Osaka':32400,'Sapporo':32400,'Seoul':32400,
                        'Tokyo':32400,'Adelaide':34200,'Darwin':34200,'Brisbane':36000,'Canberra':36000,'Guam':36000,'Hobart':36000,'Melbourne':36000,
                        'Port Moresby':36000,'Sydney':36000,'Yakutsk':36000,'New Caledonia':39600,'Solomon Is':39600,'Vladivostok':39600,'Auckland':43200,
                        'Fiji':43200,'Kamchatka':43200,'Magadan':43200,'Marshall Is':43200,'Wellington':43200,"nuku'alofa":46800, "None":0}
        return     TimeZoneList[timezone]
    
    def doParsing(self,fileName,file):
        countTweets = 0
        with open(fileName) as json_data:
            
            data = json.load(json_data)
            fileNameWithOutType = file.split(".")[0]
            parsed_file = "C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\parsed\\hourWiseTweetCount\\"+fileNameWithOutType+".csv"
            for obj in data:
                temp = obj
                x_str = str(temp)
                word = 'created_at'
                if word in x_str:
                    countTweets = countTweets + 1
                    #print("Tweet no:",countTweets)
                    tempCreated = ((str(obj['created_at'])))
                    tempCreatedParsed = tempCreated.split(" ")[0]
                    self.created_day_list.append(TweetsOfAParticularTime.getDay(1,tempCreatedParsed))
                    
                    tempCreatedParsed = tempCreated.split(" ")[1]
                    self.created_month_list.append(TweetsOfAParticularTime.getMonth(1,tempCreatedParsed))
                    
                    tempCreatedParsed = int(tempCreated.split(" ")[2])
                    self.created_date_list.append(tempCreatedParsed)
                    
                    tempCreatedParsedTime = tempCreated.split(" ")[3]
                    tempCreatedParsedTimeParsed = tempCreatedParsedTime.split(':')
                    self.created_hour_list.append(tempCreatedParsedTimeParsed[0])
                    self.created_min_list.append(tempCreatedParsedTimeParsed[1])
                    self.created_sec_list.append(tempCreatedParsedTimeParsed[2])
                    
                    tempCreatedParsed = int(tempCreated.split(" ")[5])
                    self.created_year_list.append(tempCreatedParsed)  
                
                    self.id_list.append((str(obj['id'])))    
                    try:
                        self.lang_list.append(TweetsOfAParticularTime.getLanguage(1, str(obj['user']['lang'])))
                    except:
                        self.lang_list.append(0)
                    
                    
                    
            rows = zip(self.created_day_list,self.created_date_list,self.created_month_list,self.created_year_list,self.created_hour_list,self.created_min_list,
                       self.created_sec_list,self.id_list,self.lang_list)
                    
        with open(parsed_file,'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
    
            writer.writerow(["created_day_list","created_date_list","created_month_list","created_year_list","created_hour_list","created_min_list", "created_sec_list","id_list","lang_list"])
            
            try:  
                for row in rows:    
                    writer.writerow(row)
            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            except ValueError:
                print ("Could not convert data to an integer.")
            except:
                print ("Unexpected error:", sys.exc_info()[0])
        
        
        
path = 'C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\raw\\'
dirs = os.listdir( path )

for file in dirs:
    
    fileName = path+file 
    print('****************************************NEW TWEET*************************************')
    print(fileName)
    parsing = TweetsOfAParticularTime()
    parsing.doParsing(fileName,file)        
        
        