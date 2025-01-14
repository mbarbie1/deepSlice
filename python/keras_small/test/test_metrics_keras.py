# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:45:22 2018

@author: mbarbier
"""
from __future__ import print_function 
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils # numpy utils for to_categorical()
from keras import backend as K  # abstract backend API (in order to generate compatible code for Theano and Tf)
from sklearn.metrics import classification_report

batch_size = 128
nb_classes = 10
nb_epoch = 2

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

if K.image_dim_ordering() == 'th':
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

# Take a subset of 15 numbers?

X_train = X_train[0:15]
X_test = X_test[0:15]
y_train  = y_train[0:15]
y_test  = y_train[0:15]

X_train /= 255 # range [0,1]
X_test /= 255 # range [0,1]
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes) # necessary for use of categorical_crossentropy 
Y_test = np_utils.to_categorical(y_test, nb_classes) # necessary for use of categorical_crossentropy 

# create model
model = Sequential()

model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# configure model
#model.compile(loss='categorical_crossentropy',
model.compile(loss=['binary_crossentropy','binary_crossentropy','binary_crossentropy',
                    'binary_crossentropy','binary_crossentropy','binary_crossentropy',
                    'binary_crossentropy','binary_crossentropy','binary_crossentropy','binary_crossentropy'],
              optimizer='adadelta',
              metrics=['accuracy'],loss_weights=[1,10,1,1,1,1,1,1,1,1],
                weighted_metrics=['accuracy'])

# train model
model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))

# evaluate model with keras
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

# evaluate model with sklearn
predictions_last_epoch = model.predict(X_test, batch_size=batch_size, verbose=1)
target_names = ['class 0', 'class 1', 'class 2', 'class 3', 'class 4', 
                    'class 5', 'class 6', 'class 7', 'class 8', 'class 9']

predicted_classes = np.argmax(predictions_last_epoch, axis=1)
print('\n')
print(classification_report(y_test, predicted_classes, 
        target_names=target_names, digits = 6))