import sys
import os
import re
import requests
import time
from datetime import datetime

def filter_list(list):	#Checks the fourth value of each list element. 1 means too old, 0 means acceptable
	x = 0
	while x < len(list):	#Iterate over the length of each list until the end is reached
		if list[x][4] == 1:
			del(list[x])	#Remove the list element from the list
		else:
			x += 1 			#Increment counter only if element was not removed
	return list 			#Return filtered list as old list

def validate_time(items):	#Compare current time with time of timestamp. If the discrepancy is 24 hours (86400 seconds) mark with 1. Else mark with 0
	stamp = time.time()		#Get current time
	x = 0
	while x < len(items):
		if stamp - items[x][1] > 86400:		#Subtract item timestamp from current time
			items[x].append(1)
		else:
			items[x].append(0)
		x += 1 				#Increment only if no element was removed
	return items


def get_items(URL, items, names):
	postamble = '?listings=2&hq=True'	#Define the optional arguments
	Output = []
	x = 0
	while x < len(items):
	#for x in range(0, len(items)):
		sys.stdout.write(f'\rRequesting item: {items[x]}')	#sys.stdout.write to overwrite previous output
		sys.stdout.flush()
		Buffer = requests.get(URL + str(items[x]) + postamble).text	#Get data for current item from Universalis server
		try:
			time = (int(re.search(r'(?<="lastUploadTime":)[0-9]*(?=,"listings":)', Buffer).group(0))/1000)	#Use regex matching to get the item timestamp
		except AttributeError:
			continue
		price = re.search(r'(?<="minPriceHQ":)[0-9]*(?=,"maxPrice":)', Buffer).group(0)	#Use regex matching to get the price of the cheapest offer
		try:
			world = re.search(r'(?<="worldName":")[a-zA-Z]*(?="(,})?)', Buffer).group(0)#Try to get the server the item is offered on
		except AttributeError:
			world = 'Lich'		#Default to Lich if none is found
			time = 957605707	#Set time to the year 2000, marking it as too old
		Output.append([int(price)] + [int(time)] + [world] + [names[x]])	#Add new list element to list
		x += 1
	Output = validate_time(Output)	#Check the age of the datapoint
	for x in range(0, len(Output)):	#Convert the UNIX timestamp for the list to a readable date
		Output[x][1] = datetime.utcfromtimestamp(Output[x][1]).strftime('%Y-%m-%d %H:%M:%S')
	return Output


def writeout(string):	#Debug function to write data 
	with open('Test.json', 'w') as cover:
		cover.write(str(string))
		sys.exit()