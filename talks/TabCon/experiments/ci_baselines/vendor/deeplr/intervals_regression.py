import numpy as np
import gc
import scipy
from intervals_regression_xgboost import ll

def CI_NN(MVE_network, X, X_train, Y_train, alpha, n_steps=10,
          n_epochs=40, delta=1, fraction=0.1):
    """Calculate a confidence interval for all x values in X.

    This function is basically a wrapper function that calls
    CI_NNx a number of times in order to save some duplicate computations.
    """
    CI = np.zeros((len(X), 2))
    mu_hats = MVE_network.f(X_train)
    sigma_hats = MVE_network.sigma(X_train)
    for j, x in enumerate(X):
        lowerbound, upperbound = CI_NNx(MVE_network=MVE_network,
                                        x=x,
                                        X_train=X_train,
                                        Y_train=Y_train,
                                        mu_hats=mu_hats,
                                        sigma_hats=sigma_hats,
                                        delta=delta,
                                        fraction=fraction,
                                        n_steps=n_steps,
                                        n_epochs=n_epochs,
                                        alpha=alpha, )
        CI[j, 0] = lowerbound
        CI[j, 1] = upperbound
    gc.collect()
    return CI


def CI_NNx(*, MVE_network, x, X_train, Y_train, mu_hats, sigma_hats,
           n_steps, alpha, n_epochs, delta, fraction):
    # Step 1: Let the network train more to reach different values at x.
    x = np.array([x])
    start_value = MVE_network.f(x)
    MVE_network.train_on(x_new=x, X_train=X_train, Y_train=Y_train,
                         delta=delta, n_epochs=n_epochs, fraction=fraction)
    MVE_network.train_on(x_new=x, X_train=X_train, Y_train=Y_train,
                         delta=delta, positive=0, n_epochs=n_epochs, fraction=fraction)
    max_value = MVE_network.f_perturbed(x, positive=True)
    min_value = MVE_network.f_perturbed(x, positive=False)

    # The predictions of the two perturbed networks at the training locations.
    perturbed_predictions_positive = MVE_network.f_perturbed(X_train, positive=True)
    perturbed_predictions_negative = MVE_network.f_perturbed(X_train, positive=False)

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
        # Check if we can accept this
        accepting = accept(Y_train, mu_tildes, mu_hats, sigma_hats, alpha)
        # Update the upperbound if we accept
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
        accepting = accept(Y_train, mu_tildes, mu_hats, sigma_hats, alpha)
        # Update the upperbound if we accept
        if accepting:
            lowerbound = start_value * (1-l) + l * min_value
            l += 1 / n_steps
    return lowerbound, upperbound


def accept(Y, mu_0, mu_1, sigma, alpha):
    """Accept if the loglikelihoodratio < log(alpha)"""
    ratio = - loglikelihoodratio(Y, mu_0, mu_1, sigma)
    if 2*ratio > stats.chi2(1).ppf(1-alpha):
        return 0
    else:
        return 1


def loglikelihoodratio(y, mu_0, mu_hat, sigma):
    """Return the log of the likelihood ratio"""
    return -(- 0.5 * np.sum(((y - mu_hat) / sigma)**2) + 0.5 * np.sum(((y - mu_0) / sigma)**2))


def CI_NNMSEx(*, MSE_network, x, X_train, Y_train, n_steps, alpha, delta,
              n_epochs, fraction):
    # Step 1: Let the network train more to reach different values at x.
    critical_value = scipy.stats.chi2(1).ppf(1 - alpha)
    x = np.array([x])
    start_value = MSE_network.f(x)
    mu_hats = MSE_network.f(X_train)
    MSE_network.train_on(x_new=x, X_train=X_train, Y_train=Y_train,
                         delta=delta, n_epochs=n_epochs, fraction=fraction)
    MSE_network.train_on(x_new=x, X_train=X_train, Y_train=Y_train,
                         delta=delta, positive=0, n_epochs=n_epochs, fraction=fraction)
    max_value = MSE_network.f_perturbed(x, positive=True)
    min_value = MSE_network.f_perturbed(x, positive=False)

    # The predictions of the two perturbed networks at the training locations.
    perturbed_predictions_positive = MSE_network.f_perturbed(X_train, positive=True)
    perturbed_predictions_negative = MSE_network.f_perturbed(X_train, positive=False)

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
        # Check if we can accept this
        ratio = 2 * (ll(Y_train, mu_hats) - ll(Y_train, mu_tildes))
        if ratio > critical_value:
            accepting = False
        # Update the upperbound if we accept
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
