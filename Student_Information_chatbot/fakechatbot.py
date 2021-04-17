import json 
import numpy as np 
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


with open('interview.json') as file:
    data = json.load(file)


from sklearn.preprocessing import LabelEncoder


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


enc = LabelEncoder()
enc.fit(training_labels)
training_labels = enc.transform(training_labels)


vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_len)


classes = len(labels)


model = tf.keras.models.Sequential()
model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(classes, activation='softmax'))
model.summary()

training_labels_final = np.array(training_labels)

EPOCHS = 500
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=EPOCHS)

tf.keras.models.save_model(model,"mymodel.h5")

def check():
    print('start talking with bot, Enter quit to exit')
    while True:
        string = input('Enter: ')
        if string == 'quit': break
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([string]),
                                             truncating=trunc_type, maxlen=max_len))
        category = enc.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag']==category:
                print(np.random.choice(i['responses']))
                
check()





