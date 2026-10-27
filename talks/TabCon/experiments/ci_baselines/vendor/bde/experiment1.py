#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The architecture using the UCI datasets is based on
the code by Yarin Gal that he used for his article Dropout as a Bayesian Approximation.
He, in turn, based his code on the code by Jose Miguel Hernandez-Lobato.

@author: Laurens Sluijterman
"""
import argparse
import sys
import numpy as np
from datetime import date
from sklearn.model_selection import train_test_split
sys.path.append('/Users/laurens/OneDrive/Onedrivedocs/PhD/Code/2020/Bootstrapped-Deep-Ensembles')
from intervals import PICI_deep_ensemble, deep_ensemble_prediction, PICI_bootstrapped_deep_ensemble, \
    PICI_concrete_dropout, PI_QD_ensemble, CI_naive_bootstrap
from utils import load_data
from target_simulation import gen_new_targets, create_true_function_and_variance, \
    create_true_function_and_variance_NN
from neural_networks import gen_deep_ensemble, gen_extra_deep_ensemble, gen_QD_ensemble, DropoutNetwork, gen_bootstrap_ensemble
from metrics import Interval_metrics
from klepto.archives import dir_archive

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', required=True,
                    help="name of directory of dataset")
parser.add_argument('-M', '--n_ensembles', type=int,
                    required=True, help="Number of ensembles used")
parser.add_argument('-hid', '--n_hidden', type=int,
                    nargs='+', required=True, help="Number hidden units per layer")
parser.add_argument('-a', '--alphas', nargs='+', type=float, required=True,
                    help="Chosen confidence levels")
parser.add_argument('-N', '--N_simulations', type=int, default=100,
                    help='Number of simulations')
parser.add_argument('-dist', '--distribution', type=str, default=100,
                    help='Distribution to simulate data from')
parser.add_argument('-ne', '--number_of_epochs', type=int, default=40,
                    help='Number of training epochs')
parser.add_argument('-rf', '--retrain_fraction', type=float, required=True,
                    help='Fraction of epochs that training is repeated')
parser.add_argument('-sm', '--simulation_method', type=str, default='RF',
                    help='The base model to simulate targets with')
args = parser.parse_args()

n_hidden = np.array(args.n_hidden)
M = args.n_ensembles
data_directory = args.dir
alphas = args.alphas
N_simulations = args.N_simulations
distribution = args.distribution
retrain_fraction = args.retrain_fraction
simulation_method = args.simulation_method
n_epochs = args.number_of_epochs

_RESULTS_LOG = "./Results/" + data_directory + "/resultslog2.txt"
_METRICS_LOCATION = "./Results/" + data_directory + "/raw_results/PICIdata"

X, Y = load_data(data_directory)

# Create a data-generating function
if simulation_method == 'RF':
    f, var_true = create_true_function_and_variance(X, Y)
if simulation_method == 'NN':
    f, var_true = create_true_function_and_variance_NN(X, Y)

# Run the N simulations
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
N_test = len(X_test)

BDE_metrics = Interval_metrics(N_simulations, alphas, N_test)
DE_metrics = Interval_metrics(N_simulations, alphas, N_test)
Dropout_metrics = Interval_metrics(N_simulations, alphas, N_test)
QD_metrics = Interval_metrics(N_simulations, alphas, N_test)
NB_metrics = Interval_metrics(N_simulations, alphas, N_test)


error_fhati_f = np.zeros((N_simulations, N_test))
error_fhathati_fhati = np.zeros((N_simulations, N_test))

np.random.seed(1)
save_epoch = np.int(np.round(n_epochs * (1 - retrain_fraction)))

for i in range(0, N_simulations):
    print(f'Simulation {i + 1}/{N_simulations}')
    # Simulate new data
    Y_train_new = gen_new_targets(X_train, f, var_true, dist=distribution)
    Y_test = gen_new_targets(X_test, f, var_true, dist=distribution)
    f_test = f(X_test)
    sigma_test = np.sqrt(var_true(X_test))
    # Train a Deep Ensemble and Bootstrapped Deep ensemble
    deep_networks = gen_deep_ensemble(X_train, Y_train_new, M, n_hidden, n_epochs=n_epochs, save_epoch=save_epoch, verbose=0)
    extra_deep_networks = gen_extra_deep_ensemble(X_train, deep_networks, retrain_epochs=n_epochs-save_epoch)
    naive_bootstrap_networks = gen_bootstrap_ensemble(X_train, Y_train, M, n_hidden, n_epochs=n_epochs)
    # Train a Concrete Dropout network
    concrete_dropout_model = DropoutNetwork(X_train, Y_train_new, n_hidden, n_epochs=3*n_epochs, verbose=0)
    # Train Quality-driven Ensemble for each alpha
    QD_ens = []
    for alpha in alphas:
        QD_ens.append(gen_QD_ensemble(X_train, Y_train_new, M, n_hidden, alpha, n_epochs=3*n_epochs, verbose=0))
    # Calculate the relevant metrics
    error_fhati_f[i] = deep_networks[0].f(X_test) - f_test
    error_fhathati_fhati[i] = extra_deep_networks[0].f(X_test) - deep_networks[0].f(X_test)
    DE_metrics.update_bias(deep_ensemble_prediction(deep_networks, X_test), f_test, simulation=i)
    DE_metrics.update_error(deep_ensemble_prediction(deep_networks, X_test), Y_test, simulation=i)
    NB_metrics.update_error(deep_ensemble_prediction(naive_bootstrap_networks, X_test), Y_test, simulation=i)
    Dropout_metrics.update_error(concrete_dropout_model.f(X_test), Y_test,simulation=i)

    for j, alpha in enumerate(alphas):
        # Creating all the intervals
        PI_CD, CI_CD = PICI_concrete_dropout(concrete_dropout_model, X_test, alpha)
        PI_DE, CI_DE = PICI_deep_ensemble(deep_networks, X_test, alpha)
        PI_BDE, CI_BDE = PICI_bootstrapped_deep_ensemble(deep_networks, extra_deep_networks, X_test, alpha)
        PI_QD = PI_QD_ensemble(QD_ens[j], X_test)
        CI_NB = CI_naive_bootstrap(naive_bootstrap_networks, X_test, alpha)
        # Checking all the intervals
        BDE_metrics.update_CI(CI_BDE, f_test, simulation=i, alpha=j)
        BDE_metrics.update_PI(PI_BDE, f_test, sigma_test**2, distribution=distribution, simulation=i, alpha=j)

        DE_metrics.update_CI(CI_DE, f_test, simulation=i, alpha=j)
        DE_metrics.update_PI(PI_DE, f_test, sigma_test**2, distribution=distribution, simulation=i, alpha=j)

        Dropout_metrics.update_CI(CI_CD, f_test, simulation=i, alpha=j)
        Dropout_metrics.update_PI(PI_CD, f_test, sigma_test**2, distribution=distribution, simulation=i, alpha=j)

        QD_metrics.update_PI(PI_QD, f_test, sigma_test**2, distribution=distribution, simulation=i, alpha=j)

        NB_metrics.update_CI(CI_NB, f_test, simulation=i, alpha=j)


# %% Collect the metrics in a single dictionary and save them.
metrics_list = ['BDE_metrics',
                'DE_metrics',
                'Dropout_metrics',
                'QD_metrics',
                'NB_metrics',
                'alphas',
                'error_fhati_f',
                'error_fhathati_fhati',
                ]
metrics = {metric: eval(metric) for metric in metrics_list}
results = dir_archive(_METRICS_LOCATION, metrics, serialized=True)
results.dump()

# Write relevant metrics to a text file
with open(_RESULTS_LOG, "a") as myfile:
    myfile.write(f'{data_directory} M = {M},  alphas =  {alphas}, N_simulations = {N_simulations}, dist = {distribution},'
                 f' retrain_fraction={retrain_fraction}, simulation_method={simulation_method} \n')
    myfile.write(
        f'Epochs={n_epochs}\n')
    myfile.write(str(date.today()) + '\n')
    myfile.write('BRIER SCORES PREDICTION INTERVALS \n')
    myfile.write(f' Deep Ensembles              = {DE_metrics.Brier_score("PI")} \n')
    myfile.write(f' Bootstrapped Deep Ensembles = {BDE_metrics.Brier_score("PI")}  \n')
    myfile.write(f' Concrete Dropout            = {Dropout_metrics.Brier_score("PI")}  \n')
    myfile.write(f' Quality Driven Ensemble     = {QD_metrics.Brier_score("PI")}  \n')
    myfile.write('\n')
    myfile.write('BRIER SCORES CONFIDENCE INTERVALS \n')
    myfile.write(f' Deep Ensembles              = {DE_metrics.Brier_score("CI")} \n')
    myfile.write(f' Bootstrapped Deep Ensembles = {BDE_metrics.Brier_score("CI")}  \n')
    myfile.write(f' Concrete Dropout            = {Dropout_metrics.Brier_score("CI")}  \n')
    myfile.write(f' Naive Bootstrap             = {NB_metrics.Brier_score("CI")}  \n')
    myfile.write('\n')
    myfile.write('WIDTHS PREDICTION INTERVALS \n')
    myfile.write(f' Deep Ensembles              = {np.mean(np.mean(DE_metrics.PI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Bootstrapped Deep Ensembles = {np.mean(np.mean(BDE_metrics.PI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Concrete Dropout            = {np.mean(np.mean(Dropout_metrics.PI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Quality Driven Ensemble     = {np.mean(np.mean(QD_metrics.PI_width, axis=0), axis=1)}  \n')
    myfile.write('\n')
    myfile.write('WIDTHS CONFIDENCE INTERVALS \n')
    myfile.write(f' Deep Ensembles              = {np.mean(np.mean(DE_metrics.CI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Bootstrapped Deep Ensembles = {np.mean(np.mean(BDE_metrics.CI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Concrete Dropout            = {np.mean(np.mean(Dropout_metrics.CI_width, axis=0), axis=1)}  \n')
    myfile.write(f' Naive Bootstrap             = {np.mean(np.mean(NB_metrics.CI_width, axis=0), axis=1)}  \n')
    myfile.write('\n')
    myfile.write('RMSE \n')
    myfile.write(f' (Bootstrapped) Deep Ensembles = {DE_metrics.RMSE()}  \n')
    myfile.write(f' Concrete Dropout = {Dropout_metrics.RMSE()}  \n')
    myfile.write(f' Naive Bootstrap = {NB_metrics.RMSE()}  \n')
    myfile.write('\n')
    myfile.write('BIAS \n')
    myfile.write(f' (Bootstrapped) Deep Ensembles = {np.mean(DE_metrics.bias)}  \n')
    myfile.write('----- \n')
