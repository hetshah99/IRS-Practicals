# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:44:17 2020

@author: HETSHAH
"""

from __future__ import print_function, division
import nltk
import os
import random
from collections import Counter
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier, classify
 
stoplist = stopwords.words('english')
 
def init_lists(folder):
    a_list = []
    file_list = os.listdir(folder)
    for a_file in file_list:
        f = open(folder + a_file, encoding="utf8" ,errors='ignore')
        a_list.append(f.read())
    f.close()
    return a_list
 
def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(str(sentence))]
 
def get_features(text, setting):
    if setting=='bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}
 
def train(features, samples_proportion):
    train_size = int(len(features) * samples_proportion)

    train_set, test_set = features[:train_size], features[train_size:]
    print ('Training size = ' + str(len(train_set)) )
    print ('Test size = ' + str(len(test_set)) )

    classifier = NaiveBayesClassifier.train(train_set)
    return train_set, test_set, classifier
 
def evaluate(train_set, test_set, classifier):
    print ('Accuracy on the training set = ' + str(classify.accuracy(classifier, train_set)))
    print ('Accuracy of the test set = ' + str(classify.accuracy(classifier, test_set)))

 
if __name__ == '__main__' :
    # initialise the data
    spam = init_lists('enron1/spam/')
    ham = init_lists('enron1/ham/')
    all_emails = [(email, 'spam') for email in spam]
    all_emails += [(email, 'ham') for email in ham]
    random.shuffle(all_emails)
    print (  str(len(all_emails)) )
 
    all_features = [(get_features(email, ''), label) for (email, label) in all_emails]
 
    train_set, test_set, classifier = train(all_features, 0.8)
 
    evaluate(train_set, test_set, classifier)