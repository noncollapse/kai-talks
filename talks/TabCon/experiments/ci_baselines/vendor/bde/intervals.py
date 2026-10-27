#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:42:58 2020

@author: Laurens Sluijterman
"""
import numpy as np
import tensorflow_probability as tfp
from tensorflow import keras
from scipy import stats
tfd = tfp.distributions
l2 = keras.regularizers.l2


def PICI_deep_ensemble(deep_ensemble_networks, X, alpha):
    """
    Create a prediction and confidence interval for deep ensembles.

    This function uses the deep_networks to make
    confidence intervals and prediction interval at a 1-alpha significance level.

    Parameters:
        deep_ensemble_networks: The bootstrap networks that were created the
            'gen_deep_ensemble' function.
        X: The x-values at which we want a  prediction and confidence interval.
        alpha: The probability that the true mu(x) is not in our interval.

    Returns:
        PI: A len(X) by 2 array containing the minimum and maximum of the
            obtained prediction intervals.
        CI: A len(X) by 2 array containing the minimum and maximum of the
            obtained confidence intervals.
    """
    M = len(deep_ensemble_networks)
    mu_hats = np.zeros((len(X), M))
    sigma_hats = np.zeros((len(X), M))
    CI = np.zeros((len(X), 2))
    PI = np.zeros((len(X), 2))
    for i in range(M):
        mu_hats[:, i] = deep_ensemble_networks[i].f(X)
        sigma_hats[:, i] = deep_ensemble_networks[i].sigma(X)
    mu_hat = np.mean(mu_hats, axis=1)
    epistemic_variance = np.mean(mu_hats**2, axis=1) - mu_hat**2
    predictive_variance = np.mean(mu_hats**2, axis=1)\
        + np.mean(sigma_hats**2, axis=1)\
        - mu_hat**2
    z = stats.norm(0, 1).ppf(1 - alpha / 2)
    t = stats.t(M-1).ppf(1 - alpha / 2)
    CI[:, 0] = mu_hat - np.sqrt(epistemic_variance) * t
    CI[:, 1] = mu_hat + np.sqrt(epistemic_variance) * t
    PI[:, 0] = mu_hat - np.sqrt(predictive_variance) * z
    PI[:, 1] = mu_hat + np.sqrt(predictive_variance) * z
    return PI, CI


def deep_ensemble_prediction(deep_ensemble_networks, X):
    """Calculate the average prediction of the deep ensembles."""
    M = len(deep_ensemble_networks)
    mu_hats = np.zeros((M, len(X)))
    for i in range(M):
        mu_hats[i] = deep_ensemble_networks[i].f(X)
    mu_hat_star = np.mean(mu_hats, axis=0)
    return mu_hat_star


def PICI_bootstrapped_deep_ensemble(deep_ensemble_networks, extra_deep_ensemble_networks, X, alpha, N_samples=10000):
    """
        Create a prediction and confidence interval use a Bootstrapped Deep Ensemble.

        This function uses the ensemble members before and after retraining to make
        confidence intervals and prediction interval at a 1-alpha significance level.

        Parameters:
            deep_ensemble_networks: A list containing ensemble networks before
                retraining
            extra_deep_ensemble_networks: A list containing the ensemble networks
                after retraining
            X: The x-values at which we want a prediction and confidence interval.
            alpha: The probability that the true mu(x) is not in our interval.
            N_samples: The number of samples that are used to calculate
                the prediction interval.

        Returns:
            PI: A len(X) by 2 array containing the minimum and maximum of the
                obtained prediction intervals.
            CI: A len(X) by 2 array containing the minimum and maximum of the
                obtained confidence intervals.
        """
    M = len(deep_ensemble_networks)
    Y = np.zeros((M, len(X)))
    variances = np.zeros((M, len(X)))
    Z = np.zeros((M, len(X)))
    CI = np.zeros((len(X), 2))
    for i in range(0, M):
        Y[i] = deep_ensemble_networks[i].f(X)
        variances[i] = deep_ensemble_networks[i].sigma(X)**2
        Z[i] = Y[i] - extra_deep_ensemble_networks[i].f(X)

    # The confidence interval
    f_hat = np.mean(Y, axis=0)
    var2 = np.var(Y, axis=0, ddof=1)
    var1 = 1 / M * np.sum(Z**2, axis=0)
    varT = var1 + var2 / M
    t = stats.t(df=M-1).ppf(1 - alpha / 2)
    CI[:, 0] = f_hat - t * np.sqrt(varT)
    CI[:, 1] = f_hat + t * np.sqrt(varT)

    # The Prediction interval
    T_samples = stats.t.rvs(df=M-1, size=N_samples)
    T = np.zeros((len(X), N_samples))
    for i in range(len(X)):
        T[i] = T_samples
    f_hat = f_hat.reshape((len(X), 1))
    varT = varT.reshape((len(X), 1))
    loc = f_hat + np.sqrt(varT) * T
    scale = np.zeros((len(X), N_samples))
    for i in range(N_samples):
        scale[:, i] = np.sqrt(np.mean(variances, axis=0))
    dist = stats.norm(loc=loc, scale=scale)
    y_sampled = dist.rvs()
    PI = np.zeros((len(X), 2))
    PI[:, 0] = np.quantile(y_sampled, alpha / 2, axis=1)
    PI[:, 1] = np.quantile(y_sampled, 1 - alpha / 2, axis=1)
    return PI, CI


def PI_QD_ensemble(QD_ensemble_networks, X):
    """Calculate a prediction interval using Quality Driven Ensembles"""
    M = len(QD_ensemble_networks)
    alpha = QD_ensemble_networks[0].alpha
    z = stats.norm(0, 1).ppf(1 - alpha / 2)
    PI_predictions = np.zeros((M, len(X), 2))
    PI = np.zeros((len(X), 2))
    for i in range(M):
        PI_predictions[i] = QD_ensemble_networks[i].PI(X)
    PI[:, 0] = np.mean(PI_predictions, axis=0)[:, 0] - z * np.std(PI_predictions, axis=0)[:, 0]
    PI[:, 1] = np.mean(PI_predictions, axis=0)[:, 1] + z * np.std(PI_predictions, axis=0)[:, 1]
    return PI


def PICI_concrete_dropout(dropout_network, X, alpha):
    """Calculate a Prediction and Confidence interval using Concrete Dropout.

    Parameters:
        dropout_network: A trained dropout model (using the DropoutNetwork class)
        X: The X values for which to calculate the intervals
        alpha: The confidence level for the intervals.

    Returns:
        PI: The prediction intervals
        CI: The confidence intervals
    """
    f_hat = dropout_network.f(X)
    epistemic_variance = dropout_network.model_std(X)**2
    predictive_variance = dropout_network.sigma(X)**2 + epistemic_variance
    PI = np.zeros((len(X), 2))
    CI = np.zeros((len(X), 2))
    z = stats.norm(0, 1).ppf(1 - alpha / 2)
    CI[:, 0] = f_hat - np.sqrt(epistemic_variance) * z
    CI[:, 1] = f_hat + np.sqrt(epistemic_variance) * z
    PI[:, 0] = f_hat - np.sqrt(predictive_variance) * z
    PI[:, 1] = f_hat + np.sqrt(predictive_variance) * z
    return PI, CI


def CI_naive_bootstrap(bootstrapped_networks, X, alpha):
    """Calculate a CI using the naive bootstrap

    Parameters:
        bootstrapped_networks: Networks that are trained on resampled data
        X: The x values for which we want a confidence interval
        alpha: The confidence level for the intervals.

    Returns:
        CI: An array containing confidence intervals for each x.
    """
    M = len(bootstrapped_networks)
    t = stats.t(M-1).ppf(1 - alpha / 2)
    predictions = np.zeros((M, len(X)))
    CI = np.zeros((len(X), 2))
    for i in range(M):
        predictions[i] = bootstrapped_networks[i].f(X)
    CI[:, 0] = np.mean(predictions, axis=0) - t * np.std(predictions, axis=0)
    CI[:, 1] = np.mean(predictions, axis=0) + t * np.std(predictions, axis=0)
    return CI

