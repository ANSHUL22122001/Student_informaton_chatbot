import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder

with open('interview.json') as file:
    data = json.load(file)


training_sentences = []
training_labels = []
labels = []
responses = []


for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])


vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)




enc = LabelEncoder()
enc.fit(training_labels)
training_labels = enc.transform(training_labels)

new_model = tf.keras.models.load_model("mymodel.h5")


def check(string):
    result = new_model.predict(pad_sequences(tokenizer.texts_to_sequences([string]),
                                             truncating=trunc_type, maxlen=max_len))
    category = enc.inverse_transform([np.argmax(result)])
    for i in data['intents']:
        if i['tag']==category:
            return np.random.choice(i['responses'])
