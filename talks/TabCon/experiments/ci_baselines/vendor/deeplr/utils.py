import numpy as np

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
    """Load data from given directory"""
    _DATA_FILE = "./UCI_Datasets/" + directory + "/data/data.txt"
    _INDEX_FEATURES_FILE = "./UCI_Datasets/" + directory + "/data/index_features.txt"
    _INDEX_TARGET_FILE = "./UCI_Datasets/" + directory + "/data/index_target.txt"
    index_features = np.loadtxt(_INDEX_FEATURES_FILE)
    index_target = np.loadtxt(_INDEX_TARGET_FILE)
    data = np.loadtxt(_DATA_FILE)
    X = data[:, [int(i) for i in index_features.tolist()]]
    Y = data[:, int(index_target.tolist())]
    return X, Y


def CI_coverage_probability(intervals, true_values):
    """This function checks if the intervals contain the true values."""
    lower_correct = intervals[:, 0] < true_values
    upper_correct = intervals[:, 1] > true_values
    intervals_correct = lower_correct * upper_correct
    return intervals_correct

def sigmoid(x):
    if x > 0:
        return np.exp(x) / (1 + np.exp(x))
    else:
        return 1 / (1 + np.exp(-x))