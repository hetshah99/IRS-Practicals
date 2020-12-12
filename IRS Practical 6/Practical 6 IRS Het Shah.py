  
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:32:39 2020
@author: HETSHAH
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split



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

def removeDigits(inputString):
	resultString = ''.join([i for i in inputString if not i.isdigit()])
	return resultString


def removePunctuations(content):
	tokenizer = RegexpTokenizer(r'\w+')
	tokenizedContent = tokenizer.tokenize(content)
	finalContent = ""
	for word in tokenizedContent:
		finalContent += word + " "
	return finalContent




def preProcessData(content):
	content = removeStopWords(content)
	content = removeStemming(content)
	content = removeDigits(content)
	content = removePunctuations(content)
	return content

corups = []
labeledData = []

def processForDir(directoryPath):
	
	for (root, dirs, files) in os.walk(directoryPath):
		for file in files:

			with open(directoryPath+'/'+file, 'rb') as fileInput:

				content = fileInput.read().decode(errors='replace')
				content = preProcessData(content.lower())

				corups.append(content)

				labeledData.append(directoryPath.replace('../',''))


processForDir('blockchain')
processForDir('ai')
processForDir('movies')
processForDir('bank')

vectorizer = TfidfVectorizer()
final_vectorizer = vectorizer.fit_transform(corups)
final_vectorizer_array = final_vectorizer.toarray() 
X_train, X_test, Y_train, Y_test = train_test_split(final_vectorizer_array, labeledData, test_size = 0.2, random_state = 5)

print(corups)

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

iteration= [100,200,300,400,500,1000,2000]
clus=0
no_iter=0
score=0
for n_cluster in range(2, 11):
    for iteration_counter in iteration:
        kmeans = KMeans(n_clusters=n_cluster, max_iter= iteration_counter).fit(X_train)
        label = kmeans.labels_
        sil_coeff = silhouette_score(X_train, label, metric='euclidean')
        if sil_coeff > score:
            score= sil_coeff
            no_iter=iteration_counter
            clus= n_cluster
        print("For n_clusters={}, iter= {}, The Silhouette Coefficient is {}".format(n_cluster,iteration_counter,sil_coeff))



print('/n optimum value')
print(no_iter)
print(clus)    
    
kmeans = KMeans(n_clusters=clus, max_iter= no_iter).fit(X_train)
Y_predict = kmeans.predict(X_test)
print('k means center')
print(kmeans.cluster_centers_)

print('\n\nprediction on testing dataset')
print(Y_predict)
print('\n\nlabel for each document')
print(kmeans.labels_)