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

# Modification Variables #
original_dim = 784
intermediate_dim = 128
latent_dim = 2
batch_size = 35
epochs = 30
epsilon_std = 1.0

# Loss Function #
# y_true - True labels
# y_pred - Predicted labels
def nll(y_true, y_pred):
    return backend.sum(backend.binary_crossentropy(y_true, y_pred), axis=-1)

class KLDivergenceLayer(Layer):

    # Identity transform layer that adds KL divergence to the final model loss. #

    def __init__(self, *args, **kwargs):
        self.is_placeholder = True
        super(KLDivergenceLayer, self).__init__(*args, **kwargs)

    def call(self, inputs):

        mu, log_var = inputs

        kl_batch = - .5 * backend.sum(1 + log_var -
                                backend.square(mu) -
                                backend.exp(log_var), axis=-1)

        self.add_loss(backend.mean(kl_batch), inputs=inputs)

        return inputs

# Decoder - Sequential #
decoder = Sequential([
    Dense(intermediate_dim, input_dim=latent_dim, activation='relu'),
    Dense(original_dim, activation='sigmoid')
])

x = Input(shape=(original_dim,))
h = Dense(intermediate_dim, activation='relu')(x)

z_mu = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

z_mu, z_log_var = KLDivergenceLayer()([z_mu, z_log_var])
z_sigma = Lambda(lambda t: backend.exp(.5*t))(z_log_var)

eps = Input(tensor=backend.random_normal(stddev=epsilon_std,
                                   shape=(backend.shape(x)[0], latent_dim)))
z_eps = Multiply()([z_sigma, eps])
z = Add()([z_mu, z_eps])

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
        validation_data=(x_test, x_test))

# Encoder - Functional #
encoder = Model(x, z_mu)


# Pyplot for MNIST

# # display a 2D plot of the digit classes in the latent space
# z_test = encoder.predict(x_test, batch_size=batch_size)
# plt.figure(figsize=(6, 6))
# plt.scatter(z_test[:, 0], z_test[:, 1], c=y_test,
#             alpha=.4, s=3**2, cmap='viridis')
# plt.colorbar()
# plt.show()

# # display a 2D manifold of the digits
# n = 15  # figure with 15x15 digits
# digit_size = 28

# # linearly spaced coordinates on the unit square were transformed
# # through the inverse CDF (ppf) of the Gaussian to produce values
# # of the latent variables z, since the prior of the latent space
# # is Gaussian
# u_grid = np.dstack(np.meshgrid(np.linspace(0.05, 0.95, n),
#                                np.linspace(0.05, 0.95, n)))
# z_grid = norm.ppf(u_grid)
# x_decoded = decoder.predict(z_grid.reshape(n*n, 2))
# x_decoded = x_decoded.reshape(n, n, digit_size, digit_size)

# plt.figure(figsize=(10, 10))
# plt.imshow(np.block(list(map(list, x_decoded))), cmap='gray')
# plt.show()