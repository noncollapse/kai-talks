import numpy as np
import scipy
from copy import deepcopy


def ll(Y, predictions):
    """Calculate the loglikelihood up to a constant.

    The mse of the residuals is taken as estimate for the variance.

    Arguments:
        Y: The targets.
        predictions: The predicted means.

    Returns:
        loglik: The loglikelihood up to a constant.
    """
    sigma = np.sqrt(np.mean(np.square(Y - predictions)))
    loglik = np.sum(-np.log(sigma) - 0.5 * (Y - predictions)**2 / sigma**2)
    return loglik


def CI_XGBx(*, model, x, X_train, Y_train, n_steps, alpha, delta):
    """Calculate a confidence interval for an xgboost model.

    Arguments:
        model: A trained xgboost model
        x: The x-value for which a CI is calculated.
        X_train: The training covariates
        Y_train: The training targets.
        n_steps: The number of steps in which we go form the original predictions
            to the perturbed ones.
        alpha: The confidence level, a (1-alpha)*100% CI is constructed.
        delta: The perturbation height.

    Returns:
        lowerbound: The lowerbound of the CI
        upperbound: The upperbound of the CI

    """
    mu_hats = model.predict(X_train)
    critical_value = scipy.stats.chi2(1).ppf(1-alpha)
    # Step 1: Let the network train more to reach different values at x.
    x = np.array([x])
    y_pos = model.predict(x) + delta
    y_neg = model.predict(x) - delta
    Y_new_pos = np.hstack((Y_train, y_pos))
    Y_new_neg = np.hstack((Y_train, y_neg))
    X_new = np.hstack((X_train[:, 0], x))
    X_new = np.reshape(X_new, (len(X_new), 1))

    start_value = model.predict(x)
    model_pos = deepcopy(model)
    model_neg = deepcopy(model)

    model_pos.fit(X_new, Y_new_pos)
    model_neg.fit(X_new, Y_new_neg)

    max_value = model_pos.predict(x)
    min_value = model_neg.predict(x)

    # The predictions of the two perturbed models at the training locations.
    perturbed_predictions_positive = model_pos.predict(X_train)
    perturbed_predictions_negative = model_neg.predict(X_train)

    # Step 2: Check which linear combination of original and perturb explain the data well.
    upperbound = start_value
    lowerbound = start_value
    accepting = True
    l = 1 / n_steps
    while accepting:
        if start_value > max_value:
            break
        # Create a new alternative
        mu_tildes = l * perturbed_predictions_positive + (1-l) * mu_hats
        # Update the upperbound if we accept
        ratio = 2 * (ll(Y_train, mu_hats) - ll(Y_train, mu_tildes))
        if ratio > critical_value:
            accepting = False
        if accepting:
            upperbound = start_value * (1-l) + l * max_value
            l += 1 / n_steps

    accepting = True
    l = 1 / n_steps
    while accepting:
        if start_value < min_value:
            break
        # Create a new alternative
        mu_tildes = l * perturbed_predictions_negative + (1 - l) * mu_hats
        # Check if we can accept this
        ratio = 2 * (ll(Y_train, mu_hats) - ll(Y_train, mu_tildes))
        if ratio > critical_value:
            accepting = False
        if accepting:
            lowerbound = start_value * (1-l) + l * min_value
            l += 1 / n_steps
    return lowerbound, upperbound

