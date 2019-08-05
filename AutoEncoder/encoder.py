import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.models import Model, Sequential, load_model
from tensorflow.python.keras.layers import Input, Dense, Lambda, Layer, Add, Multiply
from tensorflow.python.keras import backend
from util import *
from modelConfig import *

x_test = np.load (f'./Models/{name}-x_test-COMPLETE.npy')

(a, b), (c, y_test) = mnist.load_data()
a = ''
b = ''
c = ''

encoder = Model(x, z_mu)

decoder = load_model (f'./Models/{name}-COMPLETE.h5', custom_objects={'KLDivergenceLayer': KLDivergenceLayer(), 'nll': nll})

# display a 2D plot of the digit classes in the latent space
z_test = encoder.predict(x_test, batch_size=batch_size)
plt.figure(figsize=(6, 6))
plt.scatter(z_test[:, 0], z_test[:, 1], c=y_test,
            alpha=.4, s=3**2, cmap='viridis')
plt.colorbar()
plt.show()

# display a 2D manifold of the digits
n = 15  # figure with 15x15 digits
digit_size = 28

# linearly spaced coordinates on the unit square were transformed
# through the inverse CDF (ppf) of the Gaussian to produce values
# of the latent variables z, since the prior of the latent space
# is Gaussian
u_grid = np.dstack(np.meshgrid(np.linspace(0.05, 0.95, n),
                               np.linspace(0.05, 0.95, n)))
z_grid = norm.ppf(u_grid)
x_decoded = decoder.predict(z_grid.reshape(n*n, 2))
x_decoded = x_decoded.reshape(n, n, digit_size, digit_size)

plt.figure(figsize=(10, 10))
plt.imshow(np.block(list(map(list, x_decoded))), cmap='gray')
plt.show()