#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Laurens Sluijterman
"""
import numpy as np
from scipy import stats


def CI_coverage_probability(intervals, true_values):
    """This function checks if the intervals contain the true values."""
    lower_correct = intervals[:, 0] < true_values
    upper_correct = intervals[:, 1] > true_values
    intervals_correct = lower_correct * upper_correct
    return intervals_correct


def PI_coverage_probability(intervals, true_values, true_variances, dist='Gaussian'):
    """This function checks with what probability the PI contains the true value.

    Arguments:
        intervals: The prediction intervals.
        true_values: The true function values.
        true_variances: The true variances of the additive noise.
        dist: The distribution of the additive noise.

    Returns:
        coverage_prob: The coverage probabilities of the intervals.
    """
    if dist == "Gaussian":
        coverage_prob = stats.norm.cdf((intervals[:, 1] - true_values) /
                                       np.sqrt(true_variances)) \
                        - stats.norm.cdf((intervals[:, 0] - true_values) /
                                         np.sqrt(true_variances))
        return coverage_prob
    if dist == "t3":
        coverage_prob = stats.t.cdf(np.sqrt(3) * (intervals[:, 1] - true_values) /
                                    np.sqrt(true_variances), df=3) \
                        - stats.t.cdf(np.sqrt(3) * (intervals[:, 0] - true_values) /
                                      np.sqrt(true_variances), df=3)
        return coverage_prob
    if dist == "gamma":
        k = 1 / 10
        theta = np.sqrt(10)
        coverage_prob = stats.gamma.cdf((intervals[:, 1] - true_values) /
                                        np.sqrt(true_variances) + k * theta,
                                        a=k, scale=theta) \
                        - stats.gamma.cdf((intervals[:, 0] - true_values) /
                                          np.sqrt(true_variances) + k * theta,
                                          a=k, scale=theta)
        return coverage_prob


def normalize(x, mean=None, std=None):
    """This function normalizes x using a given mean and standard deviation"""
    if mean is None:
        mean = np.mean(x, axis=0)
    if std is None:
        std = np.std(x, axis=0)
    return (x - mean) / std


def reverse_normalized(x_normalized, mean, std):
    """This function reverses the normalization done by the function 'normalize' """
    return x_normalized * std + mean


def load_data(directory):
    """Load data from given directory. This code-snipped was forked and adapted from 
    Yarin Gal's github.
    """
    _DATA_FILE = "./UCI_Datasets/" + directory + "/data/data.txt"
    _INDEX_FEATURES_FILE = "./UCI_Datasets/" + directory + "/data/index_features.txt"
    _INDEX_TARGET_FILE = "./UCI_Datasets/" + directory + "/data/index_target.txt"
    index_features = np.loadtxt(_INDEX_FEATURES_FILE)
    index_target = np.loadtxt(_INDEX_TARGET_FILE)
    data = np.loadtxt(_DATA_FILE)
    X = data[:, [int(i) for i in index_features.tolist()]]
    Y = data[:, int(index_target.tolist())]
    return X, Y
