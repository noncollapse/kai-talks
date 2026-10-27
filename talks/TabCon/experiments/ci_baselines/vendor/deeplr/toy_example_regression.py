import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy
from intervals_regression import CI_NN
from mve_network import MVENetwork
matplotlib.use("TkAgg")
matplotlib.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 17
plt.rcParams['axes.linewidth'] = 0.2


#%% Simulating data
np.random.seed(2)
size = (40, 1)
X = np.hstack((np.random.uniform(-1, -0.2, size=40), np.random.uniform(0.2, 1, size=40)))
Y = np.random.normal(loc=2*X**2, scale=0.1)
X = np.reshape(X, (80, 1))

#%% Training a model
model = MVENetwork(X=X, Y=Y, n_hidden_mean=np.array([40, 30, 20]),
                   n_hidden_var=np.array([5, 2]),
                   n_epochs=400, verbose=1, normalization=True,
                   reg_mean=1e-4, reg_var=1e-4)

#%% Visualizing the perturbation
x_star = 0.0
delta = 1
model.train_on(x_new=x_star, X_train=X, Y_train=Y, positive=True, delta=delta, n_epochs=300,
               verbose=1, fraction=1/16)
x_test = np.linspace(-1.2, 1.2, 100)
plt.plot(X, Y, 'o')
plt.plot(x_test, 2*x_test**2, linestyle='--', label=r'$f(x)$')
plt.plot(x_test, model.f(x_test), label=r'$\hat{f}(x)$')
plt.plot(x_test, model.f_perturbed(x_test, positive=True), label=r'$\tilde{f}(x)$')
plt.axvline(x_star, linestyle='dashed')
plt.legend(loc='center', bbox_to_anchor=(0.5, 1.1), ncol=3)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.tight_layout()
plt.show()


#%% Creating confidence intervals
x_test = np.reshape(np.linspace(-1.3, 1.3, 30), (30, 1))
CI = CI_NN(MVE_network=model, X=x_test, X_train=X, Y_train=Y, alpha=0.05,
           n_steps=100, n_epochs=400, delta=1, fraction=1/16)

#%% Visualizing the confidence intervals
plt.figure(dpi=200)
plt.plot(X, Y, 'o', alpha=0.2)
plt.plot(x_test, 2*x_test**2, linestyle='--', label=r'$f(x)$')
plt.plot(x_test, model.f(x_test), label=r'$\hat{f}(x)$')
plt.fill_between(x_test[:, 0], CI[:, 0], CI[:, 1], color='blue', alpha=0.2, linewidth=0.1, label=r'CI')
plt.legend(loc='center', bbox_to_anchor=(0.5, 1.1), ncol=3)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.tight_layout()
plt.show()

#%% Creating confidence intervals using an ensemble
ensemble = [MVENetwork(X=X, Y=Y, n_hidden_mean=np.array([40, 30, 20]),
                       n_hidden_var=np.array([5, 2]),
                       n_epochs=400, verbose=True, normalization=True,
                       reg_mean=1e-4, reg_var=1e-4) for _ in range(10)]

alpha = 0.05
CI_ensemble = np.zeros((len(x_test), 2))
predictions_ensemble = np.zeros((len(x_test)))
t = scipy.stats.t(df=len(ensemble)-1).ppf(1-alpha/2)
for i, x in enumerate(x_test):
    print(i)
    predictions = [model.f(np.array([x])) for model in ensemble]
    var = np.var(predictions)
    prediction = np.mean(predictions)
    CI_ensemble[i, 0] = prediction - t * np.sqrt(var)
    CI_ensemble[i, 1] = prediction + t * np.sqrt(var)
    predictions_ensemble[i] = prediction

#%% Visualizing the confidence intervals
plt.figure(dpi=200)
plt.plot(X, Y, 'o', alpha=0.2)
plt.plot(x_test, 2*x_test**2, linestyle='--', label=r'$f(x)$')
plt.plot(x_test, predictions_ensemble, label=r'$\hat{f}(x)$')
plt.fill_between(x_test[:, 0], CI_ensemble[:, 0], CI_ensemble[:, 1],
                 color='blue', alpha=0.2, linewidth=0.1, label=r'CI')
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.legend(loc='center', bbox_to_anchor=(0.5, 1.1), ncol=3)
plt.tight_layout()
plt.show()
