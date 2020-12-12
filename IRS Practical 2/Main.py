"""
 * @author HETSHAH
 * Created on Wed Jul 29 12:01:16 2020
"""

import os
from os import listdir
from os.path import isfile, join


stemming_value = {
    'Movies': 'movies',
    'films': 'films',
    'bearer':'bearer',
    'communication':'communicate',
    'uses':'uses',
    'moving':'move',
    'stories':'story',
    'entertainment':'entertain',
    'Cinemas':'Cinema',
    'weeks':'week',
    'months':'month',
    'marketed':'market',
    'disks':'disk',
    'stations':'station',
    'pictures':'picture',
    'quickly':'quick',
    'usually':'usual',
    'frames':'frame',
    'recorded':'record',
    'added':'add',
    'things':'thing',
    'writes':'write',
    'producer':'produce',
    'production':'produce',
    'cheque': 'chequ',
    'type': 'type',
    'which': 'which',
    'authorised': 'authoris',
    'encashed': 'encash',
    'means': 'mean',
    'person': 'person',
    'carries': 'carri',
    'bank': 'bank',
    'authority': 'author',
    'ask': 'ask',
    'encashment': 'encash',
    'used': 'use',
    'cash': 'cash',
    'withdrawal': 'withdraw',
    'kind': 'kind',
    'endorsable': 'endors',
    'identification': 'identif',
    'required': 'requir',
    'this': 'thi',
    'cannot': 'cannot',
    'endorsed': 'endors',
    'ie': 'ie',
    'payee': 'paye',
    'whose': 'whose',
    'name': 'name',
    'has': 'ha',
    'been': 'been',
    'mentioned': 'mention',
    'liable': 'liabl',
    'for': 'for',
    'that': 'that',
    'amount': 'amount',
    'drawer': 'drawer',
    'needs': 'need',
    'strike': 'strike',
    'mark': 'mark',
    'as': 'as',
    'be': 'be',
    'to': 'to',
    'done': 'done',
    'only': 'onli',
    'drawers': 'drawer',
    'account': 'account',
    'payees': 'paye',
    'third': 'third',
    'party': 'parti',
    'visit': 'visit',
    'submit': 'submit',
    'case': 'case',
    'crossed': 'cross',
    'must': 'must',
    'draw': 'draw',
    'two': 'two',
    'lines': 'line',
    'at': 'at',
    'left': 'left',
    'corner': 'corner',
    'a': 'a',
    'reaches': 'reach',
    'torn': 'torn',
    'condition': 'condit',
    'is': 'is',
    'called': 'call',
    'mutilated': 'mutil',
    'into': 'into',
    'or': 'or',
    'more': 'more',
    'pieces': 'piec',
    'relevant': 'relev',
    'shall': 'shall',
    'reject': 'reject',
    'declare': 'declar',
    'invalid': 'invalid',
    'confirms': 'confirm',
    'validation': 'valid',
    'corners': 'corner',
    'all': 'all',
    'important': 'import',
    'intact': 'intact',
    'may': 'may',
    'process': 'process',
    'when': 'when',
    'signature': 'signatur',
    'other': 'other',
    'fields': 'field',
    'empty': 'empti',
    'such': 'such',
    'blank': 'blank',
    'above': 'abov',
    'types': 'type',
    'cheques': 'chequ',
    'commonly': 'commonli',
    'known': 'known',
    'indian': 'indian',
    'banking': 'bank'
}

stop_words = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself',
              'yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself',
              'they','them','their','theirs','themselves','what','which','who','whom','this','that','these',
              'those','am','is','are','was','were','be','been','being','have','has','had','having','do','does',
              'did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by',
              'for','with','about','against','between','into','through','during','before','after','above','below',
              'to','from','up','down','in','out','on','off','over','under','again','further','then','once','here',
              'there','when','where','why','how','all','any','both','each','few','more','most','other','some','such',
              'no','nor','not','only','own','same','so','than','too','very','is','it','can','will','just','don',
              'should','now']
all_file_words = []

def print_data():
    for file_words in all_file_words:
        print(file_words)

for file_index in range(1, 11):
    file = open('./corpus/' + str(file_index) + '.txt', encoding="utf8")
    file_words = []
    for line in file:
        temp_word = ''
        for char in line:
            if char == ' ' and len(temp_word) > 0:
                file_words.append(temp_word.lower())
                temp_word = ''
            else:
                if char.isalnum():
                    temp_word = temp_word + char
        all_file_words.append(file_words)

print()
print_data()

print('\nStop Word Removal\n')

for file_index in range(10):
    for word in all_file_words[file_index]:
        if word in stop_words:
            all_file_words[file_index] = [current_word for current_word in all_file_words[file_index] if current_word != word]

print_data()

print('\nStemming\n')
keys = stemming_value.keys()

for file_index in range(10):
    for word_index in range(len(all_file_words[file_index])):
        word = all_file_words[file_index][word_index]
        if word in keys:
            all_file_words[file_index][word_index] = stemming_value.get(word)

print_data()

print('\nVocabulary\n')
vocabulary = set()

for file_index in range(10):
    for word_index in range(len(all_file_words[file_index])):
        word = all_file_words[file_index][word_index]
        vocabulary.add(word)

vocabulary = list(vocabulary)
vocabulary.sort()

print(vocabulary)

print('\nMatrix\n')

for file_index in range(10):
    file_words = all_file_words[file_index]
    s = 'Doc' + str(file_index + 1) + ':\t'
    for word in vocabulary:
        if word in file_words:
            s = s + '1\t'
        else:
            s = s + '0\t'
    print(s)