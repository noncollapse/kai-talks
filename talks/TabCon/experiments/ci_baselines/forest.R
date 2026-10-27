args <- commandArgs(trailingOnly=TRUE)
method <- args[1]
folder <- args[2]
seed <- as.integer(args[3])
trees <- as.integer(args[4])
threads <- as.integer(args[5])
suppressPackageStartupMessages(library(grf))
X <- as.matrix(read.csv(file.path(folder, 'X.csv'), check.names=FALSE))
Xq <- as.matrix(read.csv(file.path(folder, 'Xq.csv'), check.names=FALSE))
y <- read.csv(file.path(folder, 'y.csv'))[,1]
set.seed(seed)
started <- proc.time()[['elapsed']]
if (method == 'grf') {
  forest <- regression_forest(X, y, num.trees=trees, honesty=TRUE,
                             ci.group.size=2, num.threads=threads, seed=seed)
} else if (method == 'llf') {
  forest <- ll_regression_forest(X, y, num.trees=trees, honesty=TRUE,
                                ci.group.size=2, num.threads=threads, seed=seed)
} else stop('Unknown method')
fit_time <- proc.time()[['elapsed']] - started
# ll.lambda=NULL uses the official context-only cross-validation routine.
prediction <- predict(forest, Xq, estimate.variance=TRUE, num.threads=threads)
if (any(!is.finite(prediction$predictions)) ||
    any(!is.finite(prediction$variance.estimates)) ||
    any(prediction$variance.estimates < 0)) stop('Invalid forest mean/variance')
se <- sqrt(prediction$variance.estimates)
z <- qnorm(.975)
write.csv(data.frame(mean=prediction$predictions, lower=prediction$predictions-z*se,
                     upper=prediction$predictions+z*se, variance=prediction$variance.estimates),
          file.path(folder, 'predictions.csv'), row.names=FALSE)
jsonlite::write_json(list(grf_version=as.character(packageVersion('grf')),
                         fit_seconds=fit_time, total_seconds=proc.time()[['elapsed']]-started,
                         ll_lambda=if (method == 'llf') prediction$ll.lambda else NULL),
                    file.path(folder, 'forest_metadata.json'), auto_unbox=TRUE)
