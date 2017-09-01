import csv
import os

class CountHashTags:
    def __init__(self):    
        self.dict1 = {}
        self.dictCount = {}
        self.hashtagList = list()
        self.hashtagCount = list()
    def countHasTags(self,path):
        dirs = os.listdir( path )
        for file in dirs:
            filename = path+file
            print(filename)
            with open(filename, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                rowcount = 0
                for row in spamreader:
                    
                    if(rowcount > 0):
                        tempStr = str(row[0])     
                        x = tempStr.split(',')
                        try:
                            if x[0] in self.dict1:
                                tempCount = (self.dict1[x[0]])
                                tempCount = int(tempCount) + int(x[1])
                                self.dict1[x[0]] = tempCount
                            
                            else:
                                self.dict1[x[0]] = x[1]
                        except:
                            self.dict1[x[0]] = 0
                    rowcount = 1
            
            
        for key in self.dict1:
            self.hashtagList.append(key)
            self.hashtagCount.append(self.dict1[key])
#         
            rows = zip(self.hashtagList,self.hashtagCount)
#         parsedString = filename.split('\\')
#         parsedString = parsedString[len(parsedString)-1].split('.')[0]+'.csv'
            path_parse = 'C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\dict\\combined\\combine_30\\threshold_30.csv'    
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

path = "C:\\Users\\ahatua\\Desktop\\usm\\spring17\\Bot account\\twitter_bot\\twitter_data\\dict\\combined\\threshold_30\\"

# for file in dirs:
#     fullpath = path+file
#     print(fullpath)
    
countHashTags = CountHashTags()
countHashTags.countHasTags(path)