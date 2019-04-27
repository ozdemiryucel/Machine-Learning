import sys
import time
import xml.etree.cElementTree as ElementTree
from collections import Counter
import os
import nltk
import numpy as np
from nltk import collections
# import json
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import model_selection


words_of_technology = ['cellphone', 'computer', 'processor', 'cpu', 'ram', 'motherboard', 'graphic', 'monitor',
                       'game', 'laptop', 'keyboard', 'television', 'security', 'youtube', 'headphones',
                       'cellular', 'drone', 'receiver', 'windows', 'linux', 'programming']

commonly_used_words_by_females = ['love', 'lovely', 'loved', 'wedding', 'friend', 'friends', 'plates', 'menstruation',
                               'lipstick', 'life', 'hair', 'girl', 'girls', 'hate', 'lol', 'omg',
                               'beautiful', 'gossip', 'people', 'so', 'live', 'oh', 'happy', 'cute',
                               'funny', 'baby', 'sweet']

commonly_used_words_by_males = ['club', 'fuck', 'fucking', 'win', 'sex', 'the', 'football', 'messi', 'ronaldo']

people = []

class Person:  # who types tweet
    def __init__(self, code):

        self.code = code[:-4]
        self.truth_gender = ''
        self.tweets = []
        self.words = []
        self.types = []
        self.types_and_numbers_list = []
        self.valid_types_and_numbers = []
        self.features_array = []

    def calculate_and_store_types(self):
        for tweet in self.tweets:
            text = nltk.word_tokenize(tweet)
            liste = nltk.pos_tag(text)
            for word_and_type in liste:
                self.types.append(word_and_type[1])

        self.types_and_numbers_list = list(collections.Counter(self.types).items())

        feature_list = ['VBZ', ',', 'CD', 'JJS', 'WDT', 'VBP', '#', 'PRP$', 'JJR']
        #feature_list = [',', 'CD',   'VBP', '#', 'PRP$']

        for j in feature_list:
            self.func(j)

        self.valid_types_and_numbers.sort(key=lambda x: x[0])

        for i in self.valid_types_and_numbers:
            self.features_array.append(i[1])

        ############################################# KENDİ ÇIKARDIĞIM KELİMELERİN FEATURE OLARAK EKLENMESİ

        # avg = int(sum(self.features_array) / len(self.features_array))

        for word in commonly_used_words_by_males:
            if word in self.words:
                self.features_array.append(Counter(self.words).get(word))
            else:
                self.features_array.append(0)

        for word in words_of_technology:
            if word in self.words:
                self.features_array.append(Counter(self.words).get(word))  #
            else:
                self.features_array.append(0)  #

        for word in commonly_used_words_by_females:
            if word in self.words:
                self.features_array.append(Counter(self.words).get(word))  # okay
            else:
                self.features_array.append(0)
        #############################################

    def func(self, type_of_word):
        for i in self.types_and_numbers_list:
            if i[0] == type_of_word and type_of_word == "#":
                self.valid_types_and_numbers.append((i[0], i[1]))  # 1
                break

            elif i[0] == type_of_word and type_of_word == "PRP$":
                self.valid_types_and_numbers.append((i[0], i[1]))  # 2
                break

            elif i[0] == type_of_word:
                self.valid_types_and_numbers.append((i[0], i[1]))  # 3
                break
        else:
            self.valid_types_and_numbers.append((type_of_word, 0))

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def add_words(self, tweet):
        words = tweet.split(" ")
        for a in words:
            a = a.replace('.', '')
            a = a.replace('…', '')
            a = a.replace(',', '')
            a = a.replace('\'', '')
            a = a.replace('-', '')
            a = a.replace('_', '')
            a = a.replace('(', '')
            a = a.replace(')', '')
            a = a.replace('?', '')
            a = a.replace('!', '')
            a = a.replace('"', '')
            a = a.replace(':', '')
            if (a == ' ') or ('@' in a) or ('//' in a):
                continue
            else:
                self.words.append(a.lower())

    def show_all_tweets(self):
        print(self.code)
        for i in self.tweets:
            print(i)

    def show_all_words(self):
        print(self.code)
        for i in self.words:
            print(i)


def execute():
    print('\nStarted \n')

    print("Started to assemble information from files \n")

    number_of_executed_files = 0

    file = open('en/truth.txt', 'r')
    insanlar = file.read().split('\n')

    for filename in os.listdir('en'):

        if (number_of_executed_files / 3600 * 100) % 1 == 0:
            sys.stdout.write("\r{0}".format(number_of_executed_files / 3600 * 100))
            sys.stdout.write(" % completed")
            sys.stdout.flush()

        if not filename.endswith('.xml'):
            continue
        full_path_of_file = os.path.join('en', filename)
        tree = ElementTree.parse(full_path_of_file)
        root = tree.getroot()

        person = Person(filename)

        for documents in root:
            if documents.tag == 'documents':
                for document in documents:
                    if document.tag == 'document':
                        person.add_tweet(document.text)
                        person.add_words(document.text)

        code = filename[:-4]

        for insan in insanlar:  # person = 80127ab1a5040041989fbc343024545d:::female:::new zealand
            if code in insan:
                if 'female' in insan:
                    person.truth_gender = 'female'
                else:
                    person.truth_gender = 'male'

        person.calculate_and_store_types()

        people.append(person)

        number_of_executed_files = number_of_executed_files + 1
    file.close()

    print("\n\nFinished to assembly information from files\n")

    print('Calculation processes started')

    x = []
    for person in people:
        x.append(person.features_array)

    y = []
    for person in people:
        if person.truth_gender == 'male':
            y.append(1)
        elif person.truth_gender == 'female':
            y.append(0)


    '''with open("x.txt", "w") as outfile:
        json.dump(x, outfile)

    with open("y.txt", "w") as outfile:
        json.dump(y, outfile)'''

    #####################################################################

    x_np = np.array(x)
    y_np = np.array(y)

    print('\n--------------------- RESULTS ---------------------')

    predicted = model_selection.cross_val_predict(LogisticRegression(solver='lbfgs', max_iter=4000), x_np, y_np, cv=10)

    print("\nAccuracy: %", int(metrics.accuracy_score(y_np, predicted) * 10000) / 100)

    print()

    print(metrics.classification_report(y_np, predicted))


if __name__ == "__main__":

    start = time.time()

    execute()

    end = time.time()

    print('Finished in', int(end - start), 'seconds')
