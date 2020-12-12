# -*- coding: utf-8 -*-
"""
@author: HETSHAH
"""

def removePunctuations(inputString):
	punctuationList = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	resultString = ''
	for char in inputString:
		if char not in punctuationList:
			resultString = resultString + char
	return resultString

import os

print("Enter content to search:")
searchString = input()
searchString= removePunctuations(searchString)

words= searchString.split(" ")
count = 0
wordset=set()
for i in words:
    wordset.add(i)
    count=count+1
    
print('number of words in the sentence are :' + str(count))
print('the word list of the sentece is' + str(wordset))