PYTHONDONTWRITEBYTECODE=1
from tensorflow.python.keras import backend
from tensorflow.python.keras.layers import Input, Dense, Lambda, Layer, Add, Multiply
from tensorflow.python.keras.callbacks import Callback
from modelConfig import *

#Get Epoch Callback Class
class getEpoch(Callback):
    def __init__(self):
        super(getEpoch, self).__init__()
        self.epoch = 1

    def on_epoch_end(self, epoch, logs=None):
        self.epoch = epoch
        print (self.epoch)

    def __str__(self):
        return str(self.epoch)

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

# Loss Function #
# y_true - True labels #
# y_pred - Predicted labels #
def nll(y_true, y_pred):
    return backend.sum(backend.binary_crossentropy(y_true, y_pred), axis=-1)

# Decoder Specific
x = Input(shape=(original_dim,))
h = Dense(intermediate_dim, activation='relu')(x)

z_mu = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

(z_mu, z_log_var) = KLDivergenceLayer()([z_mu, z_log_var])

# Encoder Specific #
z_sigma = Lambda(lambda t: backend.exp(.5*t))(z_log_var)

eps = Input(tensor=backend.random_normal(stddev=epsilon_std,
                                   shape=(backend.shape(x)[0], latent_dim)))
z_eps = Multiply()([z_sigma, eps])
z = Add()([z_mu, z_eps])