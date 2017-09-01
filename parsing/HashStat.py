import csv
import os, sys
import pandas as pd
import re
            
########################################################################################################
############ I/P : A parsed file .csv file. This parsed file is obtained .json stream file #############
############ O/P : A .csv file which contains every of HashTag of the input .csv file and  #############
############ their corresponding USERID, DAY, MONTH, DATE, TIME, YEAR. #################################
############ path: Input .csv file path, hashStat: Output file path. ###################################
########################################################################################################


class HashStat: 		
	def __init__(self):
		print('Init')
		self.ListOfHashTags = []
		
		
	def remove_b(text):
		result_text = ''
		if text.startswith('b'):
			result_text = text[-3:]
		else:
			result_text = text
		return result_text




	def getDateTime(rowtext):
		
		searchString = "#"
		dateTime = []
		ListOfHashTags = []
		if searchString in str(rowtext):
			day = remove_b(rowtext[0])
			month = rowtext[1]
			date = rowtext[2]
			hour = rowtext[3][0:2]
			minute = rowtext[3][3:5]
			second = rowtext[3][6:8]
			year = rowtext[5][0:4]
	#         dateTime.append(day)
	#         dateTime.append(month)
	#         dateTime.append(date)
	#         dateTime.append(hour)
	#         dateTime.append(minute)
	#         dateTime.append(second)
	#         dateTime.append(year)
			tempDayTime = (day+month+date+hour+minute+second+year)
			#print(tempDayTime)
			#print(l)
			tokenizedString  = re.split(',',str(rowtext))
			username = tokenizedString[22]
			hashtags = re.findall(r"#(\w+)", str(rowtext))
				
			for i in range(len(hashtags)):
				tempDict = [hashtags[i], username, tempDayTime]
				ListOfHashTags.append(tempDict)
		 
		return ListOfHashTags       
	#         
	#         #dateTime.append(hashtags)    
	#     print(ListOfHashTags)
	#     print('===================')
	def readFile():
		# My code here
		print('in main')
		
		path = "...\\parsed\\"
		dirs = os.listdir( path )
		
		#print(dirs)
		count = 0
		for file in dirs:
		   file_name_parse=path+file
		   countrow = 0
		   
		   with open(file_name_parse) as csvfile:
			 spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			 ListOfHashTags = []
			 for row in spamreader:
				 countrow = countrow+1
				 if (countrow>=3) and (countrow%2 ==1):
					 if(len(getDateTime(row)) > 0 ):
						 tempData = getDateTime(row)
						 for i in range(len(tempData)):
							ListOfHashTags.append(tempData[i])

			 print(file)
			 
			 
			 
			 
			 hashStat = '...\\hashStat\\'+file+'.csv'
			 with open(hashStat,'w') as csvfile:
				 writer = csv.writer(csvfile, delimiter=',',
					 quotechar='|', quoting=csv.QUOTE_MINIMAL)
				 writer.writerow(["HashTag","user","dayTime"])
				 try:  
					for i in range(len(ListOfHashTags)):    
						writer.writerow(ListOfHashTags[i])
				 except IOError as e:
					print ("I/O error({0}): {1}".format(e.errno, e.strerror))
				 except ValueError:
					print ("Could not convert data to an integer.")
				 except:
					print ("Unexpected error:", sys.exc_info()[0])

hashStat = HashStat()
hashStat.readFile()   

       
    
    
    
    
    
    
    
    