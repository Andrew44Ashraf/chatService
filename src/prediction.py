import nltk
from nltk.stem.lancaster import LancasterStemmer
import pickle
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open('../dataset/intents.json') as file:
    data = json.load(file)
    #print data

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    print ('error loading features')

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


try:
    model.load("model.tflearn")
except:
    print 'error loading the model'


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat(ClientChat):
    print("Start talking with the bot (type quit to stop)!")
    #while True:
    #inp = input("You: ")
    #if inp.lower() == "quit":
     #   return 'Thanks'

    results = model.predict([bag_of_words(ClientChat, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    print(random.choice(responses))
    return random.choice(responses);


# if __name__ == '__main__':
#     chat()