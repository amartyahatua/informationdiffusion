import csv
import json
import re
import sys
import os


########################################################################################################
############ I/P : .json file obtained from Tweeter streaming data for a particular HashTag ############
############ O/P : Parsed .csv file#####################################################################
########################################################################################################






from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from sentiment import Sentiment
from topicModeling2_wiki  import TopicModeling
from geopy.geocoders import Nominatim

class TweetParserBasedOnHashTags:
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
        
        ## Sentiment list
        
        self.sentimentList1 = list()
        self.sentimentList2 = list()
        self.sentimentList3 = list()
        self.sentimentList4 = list()
        self.sentimentList5 = list()
        
         ## Topic modeling 
        self.model1_list = list()
        self.model2_list = list()
        self.model3_list = list()
        self.model4_list = list()
        self.model5_list = list()
        self.model6_list = list()
        self.model7_list = list()
        self.model8_list = list()
        self.model9_list = list()
        self.model10_list = list()
        
        self.model1_score_list = list()
        self.model2_score_list = list()
        self.model3_score_list = list()
        self.model4_score_list = list()
        self.model5_score_list = list()
        self.model6_score_list = list()
        self.model7_score_list = list()
        self.model8_score_list = list()
        self.model9_score_list = list()
        self.model10_score_list = list()
        
        self.mentionCountInTweet_list = list()
        self.hashCountInTweet_list = list()
        self.urlCountInTweet_list = list()
        self.reTweet_List = list()
        
        self.source_list = list()
        self.truncated_list = list()
        self.in_reply_to_status_id_list = list()
        self.in_reply_to_screen_name_list = list()
        self.in_reply_to_user_id_str_list = list()
        self.in_reply_to_user_id_list = list()
        self.in_reply_to_status_id_str_list = list()
        self.name_list = list()
        self.screen_name_list = list()
        self.user_id_list = list()
        self.name_list = list()
        self.screen_name_list = list()
        self.protected_list = list()
        self.verified_list = list()
        self.followers_count_list = list()
        self.friends_count_list = list() 
        self.listed_count_list = list()
        self.favourites_count_list = list()
        self.statuses_count_list = list()
        self.created_at_list = list()
        self.utc_offset_list = list()
        self.time_zone_list = list()
        self.geo_enabled_list = list()
        self.contributors_enabled_list = list()
        self.is_translator_list = list()
        self.profile_background_color_list = list()
        self.profile_background_image_url_list = list()
        self.profile_background_image_url_length_list = list()
        self.profile_background_image_url_root_list = list()
        self.profile_background_tile_list = list()
        self.profile_link_color_list = list()
        self.profile_sidebar_border_color_list = list()
        self.profile_sidebar_fill_color_list = list()
        self.profile_text_color_list = list()
        self.profile_use_background_image_list = list()
        self.profile_image_url_list = list()
        self.profile_image_url_len_list = list()
        self.profile_image_url_root_list = list()
        self.default_profile_list = list()
        self.default_profile_image_list = list()  
        self.following_list = list()
        self.follow_request_sent_list = list()
        self.notifications_list = list()
        self.geo_list = list()
        self.location_latitude_list = list()
        self.location_longitude_list = list()
        self.contributors_list = list()
        self.is_quote_status_list = list()
        self.retweet_count_list = list()
        self.favorite_count_list = list()
        self.favorited_list = list()
        self.retweeted_list = list()
        
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
        with open(fileName) as json_data:
            data = json.load(json_data)
            fileNameWithOutType = file.split(".")[0]
            parsed_file = "...\\parsed\\"+fileNameWithOutType+".csv"
            for obj in data:
                temp = obj
                x_str = str(temp)
                word = 'created_at'
                if word in x_str:
                    tempCreated = ((str(obj['created_at'])))
                    tempCreatedParsed = tempCreated.split(" ")[0]
                    self.created_day_list.append(TweetParserBasedOnHashTags.getDay(1,tempCreatedParsed))
                    
                    tempCreatedParsed = tempCreated.split(" ")[1]
                    self.created_month_list.append(TweetParserBasedOnHashTags.getMonth(1,tempCreatedParsed))
                    
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
                        self.lang_list.append(TweetParserBasedOnHashTags.getLanguage(1, str(obj['user']['lang'])))
                    except:
                        self.lang_list.append(0)
                    
                    
                    languageIndex = TweetParserBasedOnHashTags.getLanguage(1, str(obj['user']['lang']))
                
                
                
                    text_str = obj['text'] 
                    #print(text_str.encode("utf-8").strip())
                
                    if(languageIndex == 1 or languageIndex ==2):
                        sentimentList = Sentiment.getSentimentNLTK(text_str)
                        self.sentimentList1.append(sentimentList[0])
                        self.sentimentList2.append(sentimentList[1])
                        self.sentimentList3.append(sentimentList[2])
                        self.sentimentList4.append(sentimentList[3])
                        sentimentList = Sentiment.getSentimentsentiment140(text_str)
                        self.sentimentList5.append(sentimentList)
                        tempModelScore = TopicModeling.topicScore(1,text_str)
                        
                        self.model1_list.append(tempModelScore[0][0])
                        self.model2_list.append(tempModelScore[1][0])
                        self.model3_list.append(tempModelScore[2][0])
                        self.model4_list.append(tempModelScore[3][0])
                        self.model5_list.append(tempModelScore[4][0])
                        self.model6_list.append(tempModelScore[5][0])
                        self.model7_list.append(tempModelScore[6][0])
                        self.model8_list.append(tempModelScore[7][0])
                        self.model9_list.append(tempModelScore[8][0])
                        self.model10_list.append(tempModelScore[9][0])
                        
                        
                        self.model1_score_list.append(tempModelScore[0][1])
                        self.model2_score_list.append(tempModelScore[1][1])
                        self.model3_score_list.append(tempModelScore[2][1])
                        self.model4_score_list.append(tempModelScore[3][1])
                        self.model5_score_list.append(tempModelScore[4][1])
                        self.model6_score_list.append(tempModelScore[5][1])
                        self.model7_score_list.append(tempModelScore[6][1])
                        self.model8_score_list.append(tempModelScore[7][1])
                        self.model9_score_list.append(tempModelScore[8][1])
                        self.model10_score_list.append(tempModelScore[9][1])
                        
                        
                        
                        
                    else:
                        self.sentimentList1.append(0)
                        self.sentimentList2.append(0)
                        self.sentimentList3.append(0)
                        self.sentimentList4.append(0)
                        self.sentimentList5.append(0)
                        
                        self.model1_list.append(0)
                        self.model2_list.append(0)
                        self.model3_list.append(0)
                        self.model4_list.append(0)
                        self.model5_list.append(0)
                        self.model6_list.append(0)
                        self.model7_list.append(0)
                        self.model8_list.append(0)
                        self.model9_list.append(0)
                        self.model10_list.append(0)
                        
                        
                        self.model1_score_list.append(0)
                        self.model2_score_list.append(0)
                        self.model3_score_list.append(0)
                        self.model4_score_list.append(0)
                        self.model5_score_list.append(0)
                        self.model6_score_list.append(0)
                        self.model7_score_list.append(0)
                        self.model8_score_list.append(0)
                        self.model9_score_list.append(0)
                        self.model10_score_list.append(0)
                        
                        
                        
                        mentionParsedInTweet = str(text_str.encode("utf-8")).split("@")
                        mentionCountInTweet = len(mentionParsedInTweet)
                        self.mentionCountInTweet_list.append(mentionCountInTweet)
                        
                        hashParsedInTweet = str(text_str.encode("utf-8")).split("#")
                        hashCountInTweet = len(hashParsedInTweet)
                        self.hashCountInTweet_list.append(hashCountInTweet)
                        
                        urlParsedInTweet = str(text_str.encode("utf-8")).split("https://")
                        urlCountInTweet = len(urlParsedInTweet)
                        self.urlCountInTweet_list.append(urlCountInTweet)
                        
                        reTweetParsedTweet = TweetParserBasedOnHashTags.remove_b(self, str(text_str.encode("utf-8"))).split("'Re")
                        reTweetCountTweet = len(reTweetParsedTweet)
                        self.reTweet_List.append(reTweetCountTweet)
                        
                        tempSource = (str(obj['source'].encode('utf-8').strip()))
                        tempSource = re.findall(r'>(.+?)<', tempSource)
                        tempSource = tempSource[0]
                        tempSource = tempSource.split(" ")
                        self.source_list.append(TweetParserBasedOnHashTags.getSourceIndex(1,tempSource[len(tempSource)-1]))
                        
                        tempTruncated = str(obj['truncated']) ## Not taken
                        if (tempTruncated == 'False'):
                            self.truncated_list.append(0)
                        else:
                            self.truncated_list.append(1)
                            
                        if (str(obj['in_reply_to_status_id']) == 'None'):
                            self.in_reply_to_status_id_list.append(0)
                        else:
                            self.in_reply_to_status_id_list.append(str(obj['in_reply_to_status_id']))
                        
                        if (str(obj['in_reply_to_status_id_str']) == 'None'):
                            self.in_reply_to_status_id_str_list.append(0)
                        else:
                            self.in_reply_to_status_id_str_list.append(str(obj['in_reply_to_status_id_str']))
                        
                        #in_reply_to_user_id_list.append((str(obj['in_reply_to_user_id'])))      
                        
                        if(str(obj['in_reply_to_user_id']) == 'None'):
                            self.in_reply_to_user_id_list.append(0)
                        else:
                            self.in_reply_to_user_id_list.append(str(obj['in_reply_to_user_id']))
                        
                        
                        if(str(obj['in_reply_to_user_id_str']) == 'None'):
                            self.in_reply_to_user_id_str_list.append(0)
                        else:
                            self.in_reply_to_user_id_str_list.append(str(obj['in_reply_to_user_id_str']))  
                        
                        if (str(obj['in_reply_to_screen_name']) == 'None'):
                            self.in_reply_to_screen_name_list.append(0)
                        else:
                            self.in_reply_to_screen_name_list.append(str(obj['in_reply_to_screen_name']))
                        
                        self.name_list.append(TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['name'].encode('utf-8').strip())))    
                        self.screen_name_list.append(str(obj['user']['screen_name']))  
                        self.user_id_list.append(str(obj['user']['id']))
                        self.name_list.append(TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['name'].encode('utf-8').strip()))) 
                        self.screen_name_list.append(str(obj['user']['screen_name']))
                        
                        if(str(obj['user']['protected']) == 'False'):
                            self.protected_list.append(0)
                        else:
                            self.protected_list.append(1)
                        
                        if(str(obj['user']['verified']) == 'False'):
                            self.verified_list.append(0)
                        else:
                            self.verified_list.append(1)
                        
                        self.followers_count_list.append(str(obj['user']['followers_count']))
                        self.friends_count_list.append(str(obj['user']['friends_count']))
                        self.listed_count_list.append(str(obj['user']['listed_count']))
                        self.favourites_count_list.append(str(obj['user']['favourites_count']))
                        self.statuses_count_list.append(str(obj['user']['statuses_count']))
                        if(str(obj['user']['utc_offset']) == 'None'):
                            self.utc_offset_list.append(0)
                        else:
                            self.utc_offset_list.append(int(obj['user']['utc_offset']))
                        try:        
                            self.time_zone_list.append(TweetParserBasedOnHashTags.getTimeZone(1,str(obj['user']['time_zone'])))
                        except:
                            self.time_zone_list.append(0)
                        
                        if(str(obj['user']['geo_enabled']) == 'True'):
                            self.geo_enabled_list.append(1)
                        else:
                            self.geo_enabled_list.append(0)
                        
                        if(str(obj['user']['contributors_enabled']) == 'False'):
                            self.contributors_enabled_list.append(0)
                        else:
                            self.contributors_enabled_list.append(1)
                        
                        if(str(obj['user']['is_translator']) == 'False'):
                            self.is_translator_list.append(0)
                        else:
                            self.is_translator_list.append(1)
                        
                        profile_background_color_list_hex = TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['profile_background_color'].encode('utf-8').strip()))
                        profile_background_color_list_hex = '0x'+profile_background_color_list_hex[1:-1]
                        profile_background_color_list_int = int(profile_background_color_list_hex, 0)
                        self.profile_background_color_list.append(profile_background_color_list_int)
                        
                        
                        profile_background_image_type = str(obj['user']['profile_background_image_url'])
                        if(len(profile_background_image_type)>4):
                            profile_background_image_type_parsed = profile_background_image_type.split(".")
                            self.profile_background_image_url_list.append(TweetParserBasedOnHashTags.getImageType(1, profile_background_image_type_parsed[-1]))
                            self.profile_background_image_url_length_list.append(len(profile_background_image_type))
                            self.profile_background_image_url_root_list.append(len(((profile_background_image_type.split("//"))[1]).split("/")[0]))
                        else:
                            profile_background_image_type = 0
                            self.profile_background_image_url_list.append(0)
                            self.profile_background_image_url_length_list.append(0)
                            self.profile_background_image_url_root_list.append(0)
                        
                        if(str(obj['user']['profile_background_tile']) == 'False'):
                            self.profile_background_tile_list.append(0)
                        else:
                            self.profile_background_tile_list.append(1)
                        
                        profile_link_color_hex = TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['profile_link_color'].encode('utf-8').strip()))
                        profile_link_color_hex = '0x'+profile_link_color_hex[1:-1]
                        profile_link_color_int = int(profile_link_color_hex,0)
                        self.profile_link_color_list.append(profile_link_color_int)
                        
                        
                        profile_sidebar_border_color_hex = TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['profile_sidebar_border_color'].encode('utf-8').strip()))
                        profile_sidebar_border_color_hex = '0x'+profile_sidebar_border_color_hex[1:-1]
                        profile_sidebar_border_color_int = int(profile_sidebar_border_color_hex,0)
                        self.profile_sidebar_border_color_list.append(profile_sidebar_border_color_int)
                        
                        
                        
                        profile_sidebar_fill_color_hex = TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['profile_sidebar_fill_color'].encode('utf-8').strip()))
                        profile_sidebar_fill_color_hex = '0x'+profile_sidebar_fill_color_hex[1:-1]
                        profile_sidebar_fill_color_int = int(profile_sidebar_fill_color_hex,0)
                        self.profile_sidebar_fill_color_list.append(profile_sidebar_fill_color_int)
                        
                        profile_text_color_hex = TweetParserBasedOnHashTags.remove_b(1,str(obj['user']['profile_text_color'].encode('utf-8').strip()))
                        profile_text_color_hex = '0x'+profile_text_color_hex[1:-1]
                        profile_text_color_int = int(profile_text_color_hex,0)
                        self.profile_text_color_list.append(profile_text_color_int)
                                
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        if(str(obj['user']['profile_use_background_image']) == 'False'):
                            self.profile_use_background_image_list.append(0)
                        else:
                            self.profile_use_background_image_list.append(1)
                        
                        
                        
                        
                        profile_image_type = str(obj['user']['profile_image_url'])
                        if(len(profile_image_type)>3):
                            profile_image_type_parsed = profile_image_type.split(".")
                            self.profile_image_url_list.append(TweetParserBasedOnHashTags.getImageType(1, profile_image_type_parsed[-1]))
                            self.profile_image_url_len_list.append(len(profile_image_type))
                            self.profile_image_url_root_list.append(len(((profile_image_type.split("//"))[1]).split("/")[0]))
                            
                        else:
                            self.profile_image_url_list.append(0)
                            self.profile_image_url_len_list.append(0)
                            self.profile_image_url_root_list.append(0)
                            
                        if(str(obj['user']['default_profile']) == 'True'):
                            self.default_profile_list.append(1)
                        else:
                            self.default_profile_list.append(0)
                        
                        if(str(obj['user']['default_profile_image']) == 'True'):
                            self.default_profile_image_list.append(1)
                        else:
                            self.default_profile_image_list.append(0)
                            
                        if(str(obj['user']['following']) == 'True'):
                            self.following_list.append(1)
                        else:
                            self.following_list.append(0)
                            
                        
                        if(str(obj['user']['follow_request_sent']) == 'None'):
                            self.follow_request_sent_list.append(0)
                        else:
                            self.follow_request_sent_list.append(1)
                            
                        if(str(obj['user']['notifications']) == 'None'):
                            self.notifications_list.append(0)
                        else:
                            self.notifications_list.append(1)
                        
                        
                        if(str(obj['geo']) == 'None'):
                            self.geo_list.append(0)
                        else:
                            self.geo_list.append(1)
                        
                        
                        if obj['user']["location"] is None:
                            word_search = 'country'
                            string_place = str(obj['place'])
                            if word_search in string_place:
                                place_string = str(obj['place']['country']).encode('utf-8').strip()
                                place_string = TweetParserBasedOnHashTags.remove_b(1,place_string)
                                place_string = TweetParserBasedOnHashTags.remove_comma(1,place_string)
                                geolocator = Nominatim()
                                location = geolocator.geocode(place_string)
                                self.location_latitude_list.append(location.latitude)
                                self.location_longitude_list.append(location.longitude)
                            else:
                                self.location_latitude_list.append(0)
                                self.location_longitude_list.append(0)
                        else:
                            try:
                                location_string = (str(obj['user']["location"].encode('utf-8').strip()))
                                location_string = TweetParserBasedOnHashTags.remove_b(1,location_string)
                                location_string = TweetParserBasedOnHashTags.remove_comma(1,location_string)
                                geolocator = Nominatim()
                                location = geolocator.geocode(location_string)
                                self.location_latitude_list.append(location.latitude)
                                self.location_longitude_list.append(location.longitude)
                            except:
                                self.location_latitude_list.append(0)
                                self.location_longitude_list.append(0)
                        
                        
                        x = str(obj['contributors'])
                        
                        if(str(obj['contributors']) == 'None'):
                            self.contributors_list.append(0)
                        else:
                            self.contributors_list.append(1)
                            
                        if(str(obj['is_quote_status']) == 'False'):
                            self.is_quote_status_list.append(0)
                        else:
                            self.is_quote_status_list.append(1)
                            
                        self.retweet_count_list.append(str(obj['retweet_count']))
                        self.favorite_count_list.append(str(obj['favorite_count']))
                        
                        if(str(obj['favorited']) == 'False'):
                            self.favorited_list.append(0)
                        else:
                            self.favorited_list.append(1)
                            
                        if(str(obj['retweeted']) == 'False'):
                            self.retweeted_list.append(0)
                        else:
                            self.retweeted_list.append(1)
                        
                            
                        
                            
                       
            
                
                
            rows = zip(self.created_day_list,self.created_date_list,self.created_month_list,self.created_year_list,self.created_hour_list,self.created_min_list,
            self.created_sec_list,self.id_list,self.lang_list,self.sentimentList1,self.sentimentList2,self.sentimentList3,self.sentimentList4,
            self.sentimentList5,self.model1_list,self.model2_list,self.model3_list,self.model4_list,self.model5_list,self.model6_list,self.model7_list,
            self.model8_list,self.model9_list,self.model10_list,self.model1_score_list,self.model2_score_list,self.model3_score_list,self.model4_score_list,
            self.model5_score_list,self.model6_score_list,self.model7_score_list,self.model8_score_list,self.model9_score_list,self.model10_score_list,
            self.mentionCountInTweet_list,self.hashCountInTweet_list,self.urlCountInTweet_list,self.reTweet_List,self.source_list,self.truncated_list,
            self.in_reply_to_status_id_list,self.in_reply_to_screen_name_list,self.in_reply_to_user_id_str_list,self.in_reply_to_user_id_list,
            self.in_reply_to_status_id_str_list,self.user_id_list,
            self.protected_list,self.verified_list,self.followers_count_list,self.friends_count_list,self.listed_count_list,self.favourites_count_list,
            self.statuses_count_list,self.utc_offset_list, self.time_zone_list, self.geo_enabled_list, self.contributors_enabled_list,
            self.is_translator_list, self.profile_background_color_list, self.profile_background_image_url_list, self.profile_background_image_url_length_list, 
            self.profile_background_image_url_root_list, self.profile_background_tile_list, self.profile_link_color_list, 
            self.profile_sidebar_border_color_list,  self.profile_sidebar_fill_color_list, self.profile_text_color_list,
            self.profile_use_background_image_list, self.profile_image_url_list, self.profile_image_url_len_list, self.profile_image_url_root_list,
            self.default_profile_list,  self.default_profile_image_list,  self.following_list,self.follow_request_sent_list,  self.notifications_list, 
            self.geo_list, self.location_latitude_list, self.location_longitude_list, self.contributors_list, 
            self.is_quote_status_list, self.retweet_count_list, self.favorite_count_list, self.favorited_list, self.retweeted_list,self.name_list,self.screen_name_list)
            
            
            
            
            with open(parsed_file,'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                
                writer.writerow(["self.created_day_list","self.created_date_list","self.created_month_list","self.created_year_list",
                                 "self.created_hour_list","self.created_min_list", "self.created_sec_list","self.id_list",
                                 "self.lang_list","self.sentimentList1","self.sentimentList2","self.sentimentList3","self.sentimentList4",
                                "self.sentimentList5","self.model1_list","self.model2_list","self.model3_list","self.model4_list",
                                "self.model5_list","self.model6_list","self.model7_list","self.model8_list","self.model9_list","self.model10_list",
                                "self.model1_score_list","self.model2_score_list","self.model3_score_list","self.model4_score_list",
                                "self.model5_score_list","self.model6_score_list","self.model7_score_list","self.model8_score_list",
                                "self.model9_score_list","self.model10_score_list","self.mentionCountInTweet_list","self.hashCountInTweet_list",
                                "self.urlCountInTweet_list","self.reTweet_List","self.source_list","self.truncated_list","self.in_reply_to_status_id_list",
                                "self.in_reply_to_screen_name_list","self.in_reply_to_user_id_str_list","self.in_reply_to_user_id_list",
                                "self.in_reply_to_status_id_str_list","self.user_id_list","self.protected_list",
                                "self.verified_list","self.followers_count_list","self.friends_count_list",
                                "self.listed_count_list","self.favourites_count_list","self.statuses_count_list","self.utc_offset_list",
                                "self.time_zone_list","self.geo_enabled_list","self.contributors_enabled_list",
                                "self.is_translator_list","self.profile_background_color_list","self.profile_background_image_url_list",
                                "self.profile_background_image_url_length_list","self.profile_background_image_url_root_list",
                                "self.profile_background_tile_list","self.profile_link_color_list","self.profile_sidebar_border_color_list",
                                "self.profile_sidebar_fill_color_list","self.profile_text_color_list","self.profile_use_background_image_list",
                                " self.profile_image_url_list"," self.profile_image_url_len_list","self.profile_image_url_root_list",
                                "self.default_profile_list","  self.default_profile_image_list","self.following_list","self.follow_request_sent_list",
                                "self.notifications_list","self.geo_list","self.location_latitude_list"," self.location_longitude_list",
                                "self.contributors_list","self.is_quote_status_list","self.retweet_count_list",
                                "self.favorite_count_list","self.favorited_list","self.retweeted_list","self.name_list","self.screen_name_list"])
                try:  
                    for row in rows:    
                        writer.writerow(row)
                except IOError as e:
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                except ValueError:
                    print ("Could not convert data to an integer.")
                except:
                    print ("Unexpected error:", sys.exc_info()[0])
            
            
            
            
            
            

                
                
                
                
                
                
        
path = '...\\temp\\'
dirs = os.listdir( path )

for file in dirs:
    fileName = path+file 
    print(fileName)
    parsing = TweetParserBasedOnHashTags()
    parsing.doParsing(fileName,file)




