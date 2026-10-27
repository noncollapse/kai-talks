#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:28:32 2020

@author: Laurens Sluijterman
"""
import keras.models
import numpy as np
import tensorflow.keras.backend as K
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow import keras
from sklearn.utils import resample
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import Model
from utils import normalize, reverse_normalized
from keras import initializers
from tensorflow.keras.layers import InputSpec
from keras.layers import Lambda, Wrapper, Input, Dense, merge
from keras.models import Model



tfd = tfp.distributions
l2 = keras.regularizers.l2

class LikelihoodNetwork:
    """
    This class represents a trained neural network.

    The networks are trained using the negative loglikelihood as loss function
    and output an estimate for the mean, f, and standard deviation, sigma.

    Attributes:
        model: The trained neural network

    Methods:
        f: An estimate of the mean function, without any normalisation .
        sigma: An estimate of the standard deviation, without any normalisation.
    """

    def __init__(self, X, Y, n_hidden, n_epochs, save_epoch=0, name='None',
                 reg=True, batch_size=None, verbose=False, normalization=True):
        """
        Arguments:
            X: The unnormalized training covariates.
            Y: The unnormalized training targets
            n_hidden (array): An array containing the number of hidden units for
                each hidden layer.
            n_epochs (int): The number of training epochs
            name: The name the network is saved as after save_epoch number of
                training epochs
            save_epoch: The number of training epochs after which the model
                is saved.
            reg: The regularisation constant. If set to False,
                no regularisation is used.
            batch_size (int): The used batch size for training, if set to None
                the standard size of 32 is used.
            verbose (bool): Determines if training progress is printed.
        """
        self._normalization = normalization
        assert save_epoch < n_epochs
        if normalization is True:
            self._X_mean = np.mean(X, axis=0)
            self._X_std = np.std(X, axis=0)
            self._Y_mean = np.mean(Y, axis=0)
            self._Y_std = np.std(Y, axis=0)
            X = normalize(X)
            Y = normalize(Y)
        if save_epoch > 0:
            model = train_network(X, Y, n_hidden, save_epoch, loss=negative_log_likelihood,
                                  reg=reg, batch_size=batch_size,
                                  verbose=verbose)
            model.save(f'./savednetworks/{name}', overwrite=True)
            model.fit(X, Y, epochs=n_epochs - save_epoch, verbose=verbose)
            self.model = model
        else:
            model = train_network(X, Y, n_hidden, loss=negative_log_likelihood, n_epochs=n_epochs,
                                  reg=reg, batch_size=batch_size,
                                  verbose=verbose)
            self.model = model

    def f(self, X_test):
        """Return the mean prediction without any regularisation"""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            predictions = self.model.predict(X_test)[:, 0]
            return reverse_normalized(predictions, self._Y_mean, self._Y_std)
        else:
            return self.model.predict(X_test)[:, 0]

    def sigma(self, X_test):
        """Return the standard deviation prediction without any regularisation."""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            predictions = K.exp(self.model.predict(X_test)[:, 1]) + 1e-3
            return predictions * self._Y_std
        else:
            return K.exp(self.model.predict(X_test)[:, 1]) + 1e-3


class QDNetwork():
    """
    This class represents a trained Quality Driven Network..

    Attributes:
        model: The trained neural network
        alpha: The significance level of the intervals.

    Methods:
        PI: Calculate a prediction interval.
    """
    def __init__(self, X, Y, n_hidden, n_epochs, alpha, reg=False, batch_size=None, verbose=False, normalization=True):
        self._normalization = normalization
        self.alpha = alpha
        self.loss = QD_soft_loss(self.alpha)
        if normalization is True:
            self._X_mean = np.mean(X, axis=0)
            self._X_std = np.std(X, axis=0)
            self._Y_mean = np.mean(Y, axis=0)
            self._Y_std = np.std(Y, axis=0)
            X = normalize(X)
            Y = normalize(Y)
        model = train_network(X, Y, n_hidden, n_epochs, loss=self.loss,
                              reg=reg, batch_size=batch_size,
                              verbose=verbose)
        self.model = model

    def PI(self, X_test):
        """Calculate a prediction interval"""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            PI = self.model.predict(X_test)
            PI[:, 0] = reverse_normalized(self.model.predict(X_test)[:, 1], self._Y_mean, self._Y_std)
            PI[:, 1] = reverse_normalized(self.model.predict(X_test)[:, 0], self._Y_mean, self._Y_std)
            return PI
        else:
            PI = np.zeros((len(X_test), 2))
            PI[:, 0] = self.model.predict(X_test)[:, 1]
            PI[:, 1] = self.model.predict(X_test)[:, 0]
            return PI


class DropoutNetwork():
    """
    This class represents a trained Concrete Dropout neural network.

    The networks are trained using the negative loglikelihood as loss function
    and output an estimate for the mean, f, and standard deviation, sigma. The
    ConcreteDropout wrapper is used to apply the dropout training.

    Attributes:
        model: The trained neural network

    Methods:
        f: An estimate of the mean function, without any normalisation .
        model_std: An estimate of the model standard deviation.
        sigma: An estimate of the standard deviation, without any normalisation.
    """
    def __init__(self, X, Y, n_hidden, n_epochs, batch_size=None, verbose=False, normalization=True):
        self._normalization = normalization
        if normalization is True:
            self._X_mean = np.mean(X, axis=0)
            self._X_std = np.std(X, axis=0)
            self._Y_mean = np.mean(Y, axis=0)
            self._Y_std = np.std(Y, axis=0)
            X = normalize(X)
            Y = normalize(Y)
        model = train_dropout_network(X, Y, n_hidden, n_epochs, batch_size=batch_size, verbose=verbose)
        self.model = model

    def f(self, X_test, B=200):
        """Calculate the mean prediction"""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
        predictions = np.zeros((B, len(X_test)))
        for i in range(B):
            predictions[i] = reverse_normalized(self.model.predict(X_test)[:, 0], self._Y_mean, self._Y_std)
        return np.mean(predictions, axis=0)

    def model_std(self, X_test, B=200):
        """Calculate the standard deviation of the model uncertainty"""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
        predictions = np.zeros((B, len(X_test)))
        for i in range(B):
            predictions[i] = reverse_normalized(self.model.predict(X_test)[:, 0], self._Y_mean, self._Y_std)
        return np.std(predictions, axis=0)

    def sigma(self, X_test, B=200):
        """Calculate the standard deviation of the aleatoric uncertainty"""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            predictions = np.zeros((B, len(X_test)))
        for i in range(B):
            predictions[i] = np.sqrt(np.exp(self.model.predict(X_test)[:, 1])) * self._Y_std
        return np.mean(predictions, axis=0)


class ExtraTrainedNetwork:
    """"This class represents a network that has part of the training repeated
    with new data.

    Attributes:
        X: The new covariates.
        Y: The new targets.
        name: The name the original network was saved as.
        n_epochs: The amount of extra training.
        normalization: Boolean indicating to use normalization or not.
    """

    def __init__(self, X, Y, name, n_epochs, normalization=True):
        self._normalization = normalization
        if normalization:
            self._X_mean = np.mean(X, axis=0)
            self._X_std = np.std(X, axis=0)
            self._Y_mean = np.mean(Y, axis=0)
            self._Y_std = np.std(Y, axis=0)
            X = normalize(X)
            Y = normalize(Y)

        # Load the original network including optimizer state
        model = keras.models.load_model(f'./savednetworks/{name}',
                                        custom_objects={"negative_log_likelihood": negative_log_likelihood})
        model.fit(X, Y, epochs=n_epochs, verbose=0)  # Train the network
        self.model = model

    def f(self, X_test):
        """Return the mean prediction without any regularisation."""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            predictions = self.model.predict(X_test)[:, 0]
            return reverse_normalized(predictions, self._Y_mean, self._Y_std)
        else:
            return self.model.predict(X_test)[:, 0]

    def sigma(self, X_test):
        """Return the standard deviation prediction without any regularisation."""
        if self._normalization is True:
            X_test = normalize(X_test, self._X_mean, self._X_std)
            predictions = K.exp(self.model.predict(X_test)[:, 1]) + 1e-3
            return predictions * self._Y_std
        else:
            return K.exp(self.model.predict(X_test)[:, 1]) + 1e-3


class ConcreteDropout(Wrapper):
    """DIRECTLY COPIED FROM YARIN GALS GITHUB
    This wrapper allows to learn the dropout probability for any given input Dense layer.
    ```python
        # as the first layer in a model
        model = Sequential()
        model.add(ConcreteDropout(Dense(8), input_shape=(16)))
        # now model.output_shape == (None, 8)
        # subsequent layers: no need for input_shape
        model.add(ConcreteDropout(Dense(32)))
        # now model.output_shape == (None, 32)
    ```
    `ConcreteDropout` can be used with arbitrary layers which have 2D
    kernels, not just `Dense`. However, Conv2D layers require different
    weighing of the regulariser (use SpatialConcreteDropout instead).
    # Arguments
        layer: a layer instance.
        weight_regularizer:
            A positive number which satisfies
                $weight_regularizer = l**2 / (\tau * N)$
            with prior lengthscale l, model precision $\tau$ (inverse observation noise),
            and N the number of instances in the dataset.
            Note that kernel_regularizer is not needed.
        dropout_regularizer:
            A positive number which satisfies
                $dropout_regularizer = 2 / (\tau * N)$
            with model precision $\tau$ (inverse observation noise) and N the number of
            instances in the dataset.
            Note the relation between dropout_regularizer and weight_regularizer:
                $weight_regularizer / dropout_regularizer = l**2 / 2$
            with prior lengthscale l. Note also that the factor of two should be
            ignored for cross-entropy loss, and used only for the eculedian loss.
    """

    def __init__(self, layer, weight_regularizer=1e-6, dropout_regularizer=1e-5,
                 init_min=0.1, init_max=0.1, is_mc_dropout=True, **kwargs):
        assert 'kernel_regularizer' not in kwargs
        super(ConcreteDropout, self).__init__(layer, **kwargs)
        self.weight_regularizer = weight_regularizer
        self.dropout_regularizer = dropout_regularizer
        self.is_mc_dropout = is_mc_dropout
        self.supports_masking = True
        self.p_logit = None
        self.p = None
        self.init_min = np.log(init_min) - np.log(1. - init_min)
        self.init_max = np.log(init_max) - np.log(1. - init_max)

    def build(self, input_shape=None):
        self.input_spec = InputSpec(shape=input_shape)
        if not self.layer.built:
            self.layer.build(input_shape)
            self.layer.built = True
        super(ConcreteDropout, self).build()  # this is very weird.. we must call super before we add new losses

        # initialise p
        self.p_logit = self.layer.add_weight(name='p_logit',
                                            shape=(1,),
                                            initializer=initializers.RandomUniform(self.init_min, self.init_max),
                                            trainable=True)
        self.p = K.sigmoid(self.p_logit[0])

        # initialise regulariser / prior KL term
        assert len(input_shape) == 2, 'this wrapper only supports Dense layers'
        input_dim = np.prod(input_shape[-1])  # we drop only last dim
        weight = self.layer.kernel
        kernel_regularizer = self.weight_regularizer * K.sum(K.square(weight)) / (1. - K.sigmoid(self.p_logit[0]))
        dropout_regularizer = K.sigmoid(self.p_logit[0]) * K.log(K.sigmoid(self.p_logit[0]))
        dropout_regularizer += (1. - K.sigmoid(self.p_logit[0])) * K.log(1. - K.sigmoid(self.p_logit[0]))
        dropout_regularizer *= self.dropout_regularizer * input_dim
        regularizer = K.sum(kernel_regularizer + dropout_regularizer)
        self.layer.add_loss(regularizer)

    def compute_output_shape(self, input_shape):
        return self.layer.compute_output_shape(input_shape)

    def concrete_dropout(self, x):
        '''
        Concrete dropout - used at training time (gradients can be propagated)
        :param x: input
        :return:  approx. dropped out input
        '''
        eps = K.cast_to_floatx(K.epsilon())
        temp = 0.1

        unif_noise = K.random_uniform(shape=K.shape(x))
        drop_prob = (
            K.log(K.sigmoid(self.p_logit[0]) + eps)
            - K.log(1. - K.sigmoid(self.p_logit[0]) + eps)
            + K.log(unif_noise + eps)
            - K.log(1. - unif_noise + eps)
        )
        drop_prob = K.sigmoid(drop_prob / temp)
        random_tensor = 1. - drop_prob

        retain_prob = 1. - K.sigmoid(self.p_logit[0])
        x *= random_tensor
        x /= retain_prob
        return x

    def call(self, inputs, training=None):
        if self.is_mc_dropout:
            return self.layer.call(self.concrete_dropout(inputs))
        else:
            def relaxed_dropped_inputs():
                return self.layer.call(self.concrete_dropout(inputs))
            return K.in_train_phase(relaxed_dropped_inputs,
                                    self.layer.call(inputs),
                                    training=training)


def train_network(X_train, Y_train, n_hidden, n_epochs, loss, reg=True,
                  batch_size=None, verbose=False):
    """Train a network that outputs the mean and standard deviation.

    This function trains a network that outputs the mean and standard
    deviation. The network is trained using the negative loglikelihood
    of a normal distribution as the loss function.

    Parameters:
            X_train: A matrix containing the inputs of the training data.
            Y_train: A matrix containing the targets of the training data.
            n_hidden (array): An array containing the number of hidden units
                     for each hidden layer. The length of this array
                     specifies the number of hidden layers used for the
                     training of the main model.
            n_epochs: The amount of epochs used in training.
            reg: The regularisation that is used. If it is set to True,
                the standard of 1 / len(X) is used. If it is set to a float,
                then that value is used.
            batch_size: The batch-size used during training
            verbose (boolean): A boolean that determines if the training-
                    information is displayed.

    Returns:
        model: A trained network that outputs a mean and log of standard
            deviation.
    """
    try:
        input_shape = np.shape(X_train)[1]
    except IndexError:
        input_shape = 1
    if reg is True:
        c = 1 / len(Y_train)
    else:
        c = reg
    inputs = Input(shape=input_shape)
    inter = Dense(n_hidden[0], activation='relu',
                  kernel_regularizer=l2(c),
                  bias_regularizer=l2(0))(inputs)
    for i in range(len(n_hidden) - 1):
        inter = Dense(n_hidden[i + 1], activation='relu',
                      kernel_regularizer=keras.regularizers.l2(c))(inter)
    outputs = Dense(2, activation='linear')(inter)
    model = Model(inputs, outputs)
    model.compile(loss=loss, optimizer='adam')
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=n_epochs,
              verbose=verbose)
    return model


def train_dropout_network(X_train, Y_train, n_hidden, n_epochs, batch_size=None, verbose=False):
    """Copied from Yarin Galls github with small adaptations to be consistent with the rest of the code"""
    if K.backend() == 'tensorflow':
        K.clear_session()
    try:
        input_shape = np.shape(X_train)[1]
    except IndexError:
        input_shape = 1
    N = X_train.shape[0]
    D = 1
    l = 1e-4
    wd = l ** 2. / N
    dd = 2. / N
    input = Input(shape=input_shape)
    inter = ConcreteDropout(Dense(n_hidden[0], activation='relu'), weight_regularizer=wd, dropout_regularizer=dd)(input)
    for i in range(len(n_hidden) - 1):
        inter = ConcreteDropout(Dense(n_hidden[i + 1], activation='relu'), weight_regularizer=wd, dropout_regularizer=dd)(inter)
    output = ConcreteDropout(Dense(2), weight_regularizer=wd, dropout_regularizer=dd)(inter)
    model = Model(input, output)

    def heteroscedastic_loss(true, pred):
        mean = pred[:, :1]
        log_var = pred[:, 1:]
        precision = K.exp(-log_var)
        return K.sum(precision * (true - mean) ** 2. + log_var, -1)

    model.compile(optimizer='adam', loss=heteroscedastic_loss)
    model.fit(X_train, Y_train, epochs=n_epochs, batch_size=batch_size, verbose=verbose)
    return model


def negative_log_likelihood(targets, outputs):
    """Calculate the negative loglikelihood."""
    mu = outputs[..., 0:1]
    sigma = K.exp(outputs[..., 1:2]) + 1e-3
    y = targets[..., 0:1]
    loglik = - K.log(sigma) - 0.5 * K.square((y - mu) / sigma)
    return - loglik


def QD_soft_loss(alpha_):
    """Directly copied from Tim Pearce's Github"""
    def loss(targets, outputs):
        y_T = targets[:,0]
        y_U = outputs[:,0]
        y_L = outputs[:,1]
        N_ = tf.cast(tf.size(y_T), tf.float32)  # sample size
        lambda_ = 15.  # Taken from main.py from Pearce's github
        soften = 160  # idem
        gamma_U = tf.sigmoid((y_U - y_T) * soften)
        gamma_L = tf.sigmoid((y_T - y_L) * soften)
        gamma_ = tf.multiply(gamma_U, gamma_L)

        gamma_U_hard = tf.maximum(0., tf.sign(y_U - y_T))
        gamma_L_hard = tf.maximum(0., tf.sign(y_T - y_L))

        # lube - lower upper bound estimation
        qd_lhs_soft = tf.divide(tf.reduce_sum(tf.abs(y_U - y_L) * gamma_),
                                tf.reduce_sum(gamma_) + 0.001)  # add small noise in case 0
        PICP_soft = tf.reduce_mean(gamma_)
        qd_rhs_soft = lambda_ * tf.sqrt(N_) * tf.square(tf.maximum(0., (1. - alpha_) - PICP_soft))

        qd_loss_soft = qd_lhs_soft + qd_rhs_soft
        return qd_loss_soft
    return loss


def gen_deep_ensemble(X, Y, M, hidden_units, n_epochs=40, save_epoch=32, verbose=False, reg=True):
    """
    Train new networks by reshuffling the data and using random initialisations.

    The function trains a deep ensemble. Each network is trained on the
    same (reshuffled) data. The initialisation of the networks is random.

    Parameters:
        X: The x-values
        Y: The targets
        M: The desired number of trained deep ensemble networks.
        hidden_units: Array containing the dimensions of the hidden layers
        n_epochs: The number of training epochs.
        save_epoch: The number of epochs after which the network including
            optimizer state is saved.
        verbose: Boolean indicating to print training progress or not.
        reg: The regularisation constant. If set to True, a standard value
            of 1 / len(X) is used.

    Returns:
        deep_networks: A list containing the M bootstrap networks.

    """
    deep_ensemble = []
    for i in range(M):
        assert len(X) == len(Y)
        random_state = np.int(1000 * np.random.sample())
        X_shuffled = resample(X, replace=False, n_samples=len(X), random_state=random_state)
        Y_shuffled = resample(Y, replace=False, n_samples=len(X), random_state=random_state)
        deep_ensemble.append(LikelihoodNetwork(X_shuffled, Y_shuffled,
                                               hidden_units,
                                               name=f'ensemble_member_{i}',
                                               n_epochs=n_epochs,
                                               verbose=verbose, save_epoch=save_epoch, reg=reg))
    return deep_ensemble


def gen_extra_deep_ensemble(X, deep_ensemble_networks, retrain_epochs):
    """This function repeats part of the training of the ensemble members
     of a Deep Ensemble.

     Arguments:
         X: The covariates on which the original ensemble is trained.
         deep_ensemble_networks: The Deep Ensemble.
         retrain_epochs: The amount of epochs that is repeated.

     Return:
        An ensemble of retrained networks.
    """
    extra_deep_ensemble = []
    for i in range(len(deep_ensemble_networks)):
        Y_new = np.random.normal(loc=deep_ensemble_networks[i].f(X), scale=deep_ensemble_networks[i].sigma(X))
        extra_ensemble_network = ExtraTrainedNetwork(X, Y_new, f'ensemble_member_{i}', n_epochs=retrain_epochs)
        extra_deep_ensemble.append(extra_ensemble_network)
    return extra_deep_ensemble


def gen_QD_ensemble(X, Y, M, hidden_units, alpha, n_epochs=40, verbose=False):
    """Train an ensemble of QD networks."""
    QD_ensemble = []
    for i in range(M):
        assert len(X) == len(Y)
        random_state = np.int(1000 * np.random.sample())
        X_shuffled = resample(X, replace=False, n_samples=len(X), random_state=random_state)
        Y_shuffled = resample(Y, replace=False, n_samples=len(X), random_state=random_state)
        QD_ensemble.append(QDNetwork(X_shuffled, Y_shuffled,
                                               hidden_units, alpha=alpha,
                                               n_epochs=n_epochs,
                                               verbose=verbose))
    return QD_ensemble


def gen_bootstrap_ensemble(X, Y, M, hidden_units, n_epochs=40, verbose=False, reg=True):
    """
    Train new networks by reshufling the data with replacement.

    The function trains a deep ensemble. Each network is trained on the
    same (reshuffled) data. The initialisation of the networks is random.

    Parameters:
        X: The x-values
        Y: The targets
        M: The desired number of trained deep ensemble networks.
        hidden_units: Array containing the dimensions of the hidden layers
        n_epochs: The number of training epochs.
        verbose: Boolean indicating to print training progress or not.
        reg: The regularisation constant. If set to True, a standard value
            of 1 / len(X) is used.

    Returns:
        bootstrap_networks: A list containing the M bootstrap networks.

    """
    bootstrap_ensemble = []
    for i in range(M):
        assert len(X) == len(Y)
        random_state = np.int(1000 * np.random.sample())
        X_shuffled = resample(X, replace=True, n_samples=len(X), random_state=random_state)
        Y_shuffled = resample(Y, replace=True, n_samples=len(X), random_state=random_state)
        bootstrap_ensemble.append(LikelihoodNetwork(X_shuffled, Y_shuffled,
                                               hidden_units,
                                               n_epochs=n_epochs,
                                               verbose=verbose, reg=reg))
    return bootstrap_ensemble



