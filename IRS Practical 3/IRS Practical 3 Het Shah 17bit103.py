

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt




import pandas as pd

import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

def fileExists(fileName):
	if(os.path.exists(fileName)):
		return True
	else:
		return False

def getFileContent(fileName):
	with open(fileName) as inputFile:
		fileContent = inputFile.read().lower()
		return fileContent

def removeStopWords(content):
	stopWords = set(stopwords.words('english'))
	wordTokens = word_tokenize(content)
	filteredContent = [word for word in wordTokens if not word in stopWords]
	filteredContent = []
	for word in wordTokens:
		if word not in stopWords:
			filteredContent.append(word)
	finalContent = ""
	for word in filteredContent:
		finalContent += word + " "
	return finalContent

def removeStemming(content):
	posterStemmer = PorterStemmer()
	wordList = word_tokenize(content)
	resultContent = ""
	for word in wordList:
		resultContent += posterStemmer.stem(word) + " "
	
	return resultContent


def removePunctuations(content):
	tokenizer = RegexpTokenizer(r'\w+')
	tokenizedContent = tokenizer.tokenize(content)
	finalContent = ""
	for word in tokenizedContent:
		finalContent += word + " "
	return finalContent


def writeFile(data, fileName):
	preProcessedFile = open(fileName, 'w')
	preProcessedFile.write(data)
	preProcessedFile.close()

def removeDigits(inputString):
	resultString = ''.join([i for i in inputString if not i.isdigit()])
	return resultString

def processFile(fileName):
	fileContent = getFileContent(fileName)
	tokenizedContent = removePunctuations(fileContent)
	removedDigitsContent = removeDigits(tokenizedContent)
	unstemmedContent = removeStemming(removedDigitsContent)
	finalContent = removeStopWords(unstemmedContent)
	processedFileName = fileName.replace('.txt','')
	writeFile(finalContent, processedFileName + '-processed.txt')



fileName = input("Enter file name:")
# fileName = '001.txt'
if(fileExists(fileName)):
	processFile(fileName)
	print("Done processing and saved successfully!")
else:
	print("Error file doesn't exist")
    
    
fileName=fileName.replace('.txt','')
path = fileName + '-processed.txt'
data_train = pd.read_csv(path, )

import glob 
files = data_train
print(files)



all=[]
totwords=[]
fi=[]
gra={}
data=""
for file in files:                  
    fi.append(str(file))
#     with open(file) as f:
p = PorterStemmer()        
word=[]
words=[]
#new=f.read();
word=nltk.word_tokenize(str(data_train));
#print("STEMMING:")
for w in word:
    #print(p.stem(w))
    words.append(p.stem(w))

stops=['of','if','the','them','this','there','his','her']

for s in stops:
    if s in words:
        words.remove(s)
a={}
words.sort()
for w in words:
    a.setdefault(w,0)
    a[w]+=1
    if w not in totwords:
        data=data+"\n"+w
        totwords.append(w)

all.append(a)
totwords.sort()




for i in range(0,len(all)):
    dict={}
    dict=all[i]

for tot in totwords:
    dict.setdefault(tot,0)
    gra.setdefault(tot,0)
    gra[tot]=dict.get(tot)

#print(all)
print("\nTOTAL WORDS : ")

print(gra)
plt.xticks(rotation='vertical')
plt.bar(gra.keys(),gra.values(),color='g')
plt.show()

wdc=WordCloud(width=1000,height=1000,background_color='white',
              stopwords=STOPWORDS,min_font_size=10).generate(data)

plt.figure(figsize=(7,7),facecolor=None)
plt.imshow(wdc)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()