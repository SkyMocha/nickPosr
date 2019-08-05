# # # # # # # # # #
# Modified from:
# https://tiao.io/post/tutorial-on-variational-autoencoders-with-a-concise-keras-implementation/#fn:1
# # # # # # # # # # # # 
# Nicolas Kychenthal #
# # # # # # # # # # # 

# Notes #
# Current Objectives
# Gather mp3; convert to MIDI; convert to txt; edit txt to 1 character
# Convert Music into Images
# https://youtu.be/nA3YOFUCn4U?t=152
# Modify code to work with the musical images
# Work on decoding system to generate music

# Imports #
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

import tensorflow as tf

from tensorflow.python.keras.layers import Input, Dense, Lambda, Layer, Add, Multiply
from tensorflow.python.keras.models import Model, Sequential
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras import backend
from tensorflow.python.keras import callbacks

from util import *
from modelConfig import *

from time import time

conf = tf.compat.v1.ConfigProto(
      intra_op_parallelism_threads=1,
      inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session (config=conf)

#callbacks
epoch = getEpoch()
tensorboard = callbacks.TensorBoard(log_dir=f'../Logs/{name}')
checkpoint = callbacks.ModelCheckpoint(f"../Models/{name}-{epoch}.h5", monitor='val_loss', mode='auto', period=10)

# Decoder - Sequential #
decoder = Sequential([
    Dense(intermediate_dim, input_dim=latent_dim, activation='relu'),
    Dense(original_dim, activation='sigmoid')
])

x_pred = decoder(z)

vae = Model(inputs=[x, eps], outputs=x_pred)
vae.compile(optimizer='rmsprop', loss=nll)

# train the VAE on MNIST digits
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, original_dim) / 255.

x_test = x_test.reshape(-1, original_dim) / 255.

vae.fit(x_train,
        x_train,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_test, x_test),
        callbacks=[tensorboard, checkpoint, epoch])

vae.save(f'./Models/{name}-COMPLETE.h5')

np.save(f'./Models/{name}-x_test-COMPLETE.npy', x_test)