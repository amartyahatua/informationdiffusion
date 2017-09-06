import csv
import json
import re
import sys
import os

#############################################################
##############Extract hashtags from tweets###################
#############################################################

class ExtractHashTags:
    def __init__(self):    
        self.created_day_list = list()
        self.created_date_list = list()
        self.created_month_list = list()
        self.created_year_list = list()
        self.created_hour_list = list()
        self.created_min_list = list()
        self.created_sec_list = list()
        self.hashtag_list = list()
    def remove_comma(self,text):
        word_search = ','
        result_text = ''
        if word_search in text:
            result_text = text.replace(',', ' ')
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
        languageList = {'en':1,'en-gb':2,'ar':3,'bn':4,'cs':5,'da':6,'de':7,'el':8,'es':9,'fa':10,'fi':11,'fil':12,'fr':13,'he':14,'hi':15,'hu':16,'id':17,'it':18,'ja':19,'ko':20,'msa':21,'nl':22,'no':23,'pl':24,'pt':25,'ro':26,'ru':27,'sv':28,'th':29,'tr':30,'uk':31,'ur':32,'vi':33,'zh-cn':34,'zh-tw':35, 'pt-PT':36, 'zh':37, 'ca':38, 'gl':39, 'sr':40}
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
    
    def doExtraction(self,file_name_parse):
        with open(file_name_parse) as json_data:
            data = json.load(json_data)
            for obj in data:
                temp = obj
                x_str = str(temp)
                word = 'created_at'
                if word in x_str:
                    text_str = obj['text'] 
                    hashParsedInTweet = str(text_str.encode("utf-8")).split("#")
                    hashCountInTweet = len(hashParsedInTweet)
                    
                    try:
                        if (hashCountInTweet > 1):
                            result = re.findall(r"#(\w+)", text_str)
                            #print(result)
                            
                            for i in range(len(result)):
                                if(ExtractHashTags.isEnglish(self, result[i]) == 1):
                                    self.hashtag_list.append(result[i])
                                    
                                    tempCreated = ((str(obj['created_at'])))
                                    tempCreatedParsed = tempCreated.split(" ")[0]
                                    self.created_day_list.append(ExtractHashTags.getDay(1,tempCreatedParsed))
                                    
                                    tempCreatedParsed = tempCreated.split(" ")[1]
                                    self.created_month_list.append(ExtractHashTags.getMonth(1,tempCreatedParsed))
                                    
                                    tempCreatedParsed = int(tempCreated.split(" ")[2])
                                    self.created_date_list.append(tempCreatedParsed)
                                    
                                    tempCreatedParsedTime = tempCreated.split(" ")[3]
                                    tempCreatedParsedTimeParsed = tempCreatedParsedTime.split(':')
                                    self.created_hour_list.append(tempCreatedParsedTimeParsed[0])
                                    self.created_min_list.append(tempCreatedParsedTimeParsed[1])
                                    self.created_sec_list.append(tempCreatedParsedTimeParsed[2])
                                    
                                    tempCreatedParsed = int(tempCreated.split(" ")[5])
                                    self.created_year_list.append(tempCreatedParsed)   
                    except:
                        print("")            


            
            rows = zip(self.hashtag_list,self.created_day_list,self.created_date_list,self.created_month_list,self.created_year_list,self.created_hour_list,self.created_min_list,self.created_sec_list)              
            for i in range(len(self.hashtag_list)):
                x = self.hashtag_list[i]
            
            
            parsedString = file_name_parse.split('\\')
            parsedString = parsedString[len(parsedString)-1].split('.')[0]+'.csv'
            path_parse = '...\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\hashStat\\Day-6\\'+parsedString
#             length_path = (len(file_name_parse.split('\\')))
#             #print(length_path)
#             file_name = (file_name_parse.split('\\')[length_path-1])
#             file_name = file_name.split('.')
#             parsed_file = path_parse+file_name[0]+'.csv'
                
        
            with open(path_parse,'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                 
                writer.writerow(["hashtag_list","created_day_list","created_date_list","created_month_list","self.created_year_list","created_hour_list","created_min_list","created_sec_list"])
                try:  
                    for row in rows:    
                        writer.writerow(row)
                except IOError as e:
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                except ValueError:
                    print ("Could not convert data to an integer.")
                except:
                    print ("Unexpected error:", sys.exc_info()[0])
        
        
path = "...\\spring17\\Bot account\\twitter_bot\\twitter_data\\raw\Day-6_24\\"
dirs = os.listdir( path )
count = 0
for file in dirs:
   file_name_parse  = path+file
   print (file_name_parse)
   count = count + 1        
   extractHtags = ExtractHashTags()
   extractHtags.doExtraction(file_name_parse)
