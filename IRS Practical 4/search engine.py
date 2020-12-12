# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 18:13:46 2020

@author: HETSHAH
"""
import nltk
import string
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os
import numpy as np
import math
import heapq
import json
from tkinter import *
from tkinter import ttk

data = ""
tokens = []
corpus = []
wordfreq = {}
word_idf_values = {}
word_tf_values = {}
tfidf_values = []
tfidf = {}
current_path = os.getcwd()
thisdict= {}
    
def IDF():
    global data, tokens, corpus, wordfreq, word_idf_values, word_tf_values, tfidf_values, tfidf, current_path
    for word in wordfreq:
        count = 0
        for file_name in os.listdir(current_path):
            if file_name.endswith('txt'):
                file = open(file_name, encoding="utf8")
                temp_data = file.read()
                temp_tokens = nltk.word_tokenize(temp_data)
                if word in temp_tokens:
                    count += 1
                file.close()
        word_idf_values[word] = np.log(10 / (1 + count))
    
def TF():
    global data, tokens, corpus, wordfreq, word_idf_values, word_tf_values, tfidf_values, tfidf, current_path
    for word in wordfreq:
        tf_vector=[]
        for file_name in os.listdir(current_path):
            if file_name.endswith('txt'):
                freq = 0
                file = open(file_name, encoding="utf8")
                temp_data = file.read()
                temp_tokens = nltk.word_tokenize(temp_data)
                for w in temp_tokens:
                    if word == w:
                        freq += 1
                word_tf = freq / len(temp_tokens)
                tf_vector.append(word_tf)
                file.close()
        word_tf_values[word] = tf_vector

def TF_IDF():
    global data, tokens, corpus, wordfreq, word_idf_values, word_tf_values, tfidf_values, tfidf, current_path
    i = 0
    for word in word_tf_values.keys():
        temp_tfidf=[]
        for sen in word_tf_values[word]:
            score = sen * word_idf_values[word]
            temp_tfidf.append(score)
        tfidf_values.append(temp_tfidf)
        tfidf[word] = i
        i += 1
        

def preprocessing():
    global data, tokens, corpus, wordfreq, word_idf_values, word_tf_values, tfidf_values, tfidf, current_path,thisdict
    json_data = {}
    ans = []
    i=1
    for file_name in os.listdir():
        if file_name.endswith('txt'):
            file = open(file_name, encoding="utf8")
            ans.append(file.read())
            thisdict[i]=file_name
            i=i+1
            file.close()
    data = "".join(i for i in ans)
    data.lower()
    data = "".join([char for char in data if char not in string.punctuation])
    tokens = word_tokenize(data)
    tokens = [word for word in tokens if not word in stopwords.words()]
    
    
    for file_name in os.listdir(current_path):
        if file_name.endswith('txt'):
            print(file_name)
            file = open(file_name, encoding="utf8")
            temp_data = file.read()
            temp_tokens = nltk.word_tokenize(temp_data)
            for temp_token in temp_tokens:
                if temp_token in tokens and temp_token not in wordfreq.keys():
                    wordfreq[temp_token] = 1
                elif temp_token in tokens:
                    wordfreq[temp_token] += 1
            file.close()
 
    IDF()
    TF()    
    TF_IDF()
    json_data['preprocessing'] = {}
    json_data['preprocessing']['data'] = data
    json_data['preprocessing']['tokens'] = tokens
    json_data['preprocessing']['corpus'] = corpus
    json_data['preprocessing']['wordfreq'] = wordfreq
    json_data['preprocessing']['word_idf_values'] = word_idf_values
    json_data['preprocessing']['word_tf_values'] = word_tf_values
    json_data['preprocessing']['tfidf_values'] = tfidf_values
    json_data['preprocessing']['tfidf'] = tfidf
    with open('json_data.json', 'w') as outfile:
        json.dump(json_data, outfile)

def search():
    global thisdict
    canvas.delete("all")
    infile = open("json_data.json", 'r')
    json_data = json.load(infile)
    infile.close()
    data = json_data['preprocessing']['data']
    tokens = json_data['preprocessing']['tokens']
    corpus = json_data['preprocessing']['corpus']
    wordfreq = json_data['preprocessing']['wordfreq']
    word_idf_values = json_data['preprocessing']['word_idf_values']
    word_tf_values = json_data['preprocessing']['word_tf_values']
    tfidf_values = json_data['preprocessing']['tfidf_values']
    tfidf = json_data['preprocessing']['tfidf']
    
    tf_idf_model = np.asarray(tfidf_values)
    tf_idf_model = np.transpose(tf_idf_model)
    det = []
    for row in tf_idf_model:
        sum = 0
        for num in row:
            sum += num ** 2
        sum = math.sqrt(sum)
        det.append(sum)
    s = searchEntry.get()
    s.lower()
    s = nltk.word_tokenize(s)
    s = [word for word in s if not word in nltk.corpus.stopwords.words()]
    l = len(s)
    arr = []
    dic = {}
    for i in range(tf_idf_model.shape[0]):
        sum = 0.0
        for word in s:
            index = 0
            if word in tfidf.keys():
                index = tfidf[word]
                sum += tf_idf_model[i][index]
        arr.append(sum / (det[i] * math.sqrt(l)))
        dic[i] = sum / (det[i] * math.sqrt(l))
    heapq.heapify(arr)
    ans=[]
    print(dic)
    ans=heapq.nlargest(10,arr)
    print(ans)
    print_text = ""
    for i in ans:
        id = 0
        if i == 0:
            break;
        for ind, val in dic.items():
            if val == i:
                id = ind
                break
   
        print_text += ("Document: " + str(thisdict[id+1]) + "                   " + str(i) + "\n")
    canvas.create_text(50, 90, anchor=W, font="Ubuntu", text="\n\nSearch Results: \n\n" + print_text)
    
    
preprocessing()
root = Tk()
root.title("Search Engine")

root.config(bg="#2E2E2E")

UI_frame = Frame(root, width=600, height=200, bg='#ececec')
UI_frame.grid(row=3, column=0, pady=50)

canvas = Canvas(root, width=800, height=500, bg="#ececec")
canvas.grid(row=2, column=0, pady=5)

searchEntry = Entry(UI_frame)
searchEntry.grid(row=1, column=1, padx=5, pady=15, sticky=W)
Button(UI_frame, text='Click to search',command = search, bg='coral').grid(row=1,column=2,padx=5,pady=15)

root.mainloop()