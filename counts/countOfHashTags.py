import csv
import os

class CreateHasTagCount:
    def __init__(self):    
        self.dict = {}
        self.dictCount = {}
        self.hashtagList = list()
        self.hashtagCount = list()
    def countHasTags(self,file_name_parse):  
        
        
        #print (file_name_parse)
        with open(file_name_parse, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rowcount = 0
            for row in spamreader:
                tempStr = str(row[0])     
                x = tempStr.split(',')
                if x[0] in self.dict:
                    self.dict[x[0]].append(x[1])
                    try:
                        self.dict[x[0]].append(x[2])
                    except IndexError:
                        self.dict[x[0]].append('none')
                else:
                    self.dict[x[0]] = x[1:3]
 
 
        self.dictCount = {}
        for key in self.dict:
            lenOfValue = len(self.dict[key])
            if lenOfValue in self.dictCount:
                tempValue = str(self.dictCount[lenOfValue])
                tempValue = tempValue + ',' + key
                self.dictCount[lenOfValue] = tempValue
            else:
                self.dictCount[lenOfValue] = key
             
        for key in self.dict:
            self.hashtagList.append(key)
            self.hashtagCount.append(len(self.dict[key]))
             
     
        #print(self.hashtagList)
        #print(self.hashtagCount)
     
        rows = zip(self.hashtagList,self.hashtagCount)
        parsedString = file_name_parse.split('\\')
        parsedString = parsedString[len(parsedString)-1].split('.')[0]+'.csv'
        path_parse = '..\\twitter_bot\\twitter_data\\hashStat\\result\\'+parsedString    
        with open(path_parse,'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
                      
            writer.writerow(["hashtagList","hashtagCount"])
            try:  
                for row in rows:    
                    writer.writerow(row)
            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            except ValueError:
                print ("Could not convert data to an integer.")
            except:
                print ("Unexpected error:", sys.exc_info()[0])
    
path = "..\\twitter_bot\\twitter_data\\hashStat\\count2\\"
dirs = os.listdir( path )
for file in dirs:
    fullpath = path+file
    print(fullpath)
    
    countHashTags = CreateHasTagCount()
    countHashTags.countHasTags(fullpath)
     
    
    
    
    
    