args <- commandArgs(trailingOnly=TRUE)
folder <- args[1]
cfg <- jsonlite::read_json(file.path(folder, 'config.json'), simplifyVector=TRUE)
X <- as.matrix(read.csv(file.path(folder, 'X.csv'), check.names=FALSE))
Xq <- as.matrix(read.csv(file.path(folder, 'Xq.csv'), check.names=FALSE))
y <- read.csv(file.path(folder, 'y.csv'))[,1]
set.seed(as.integer(cfg$seed))
started <- proc.time()[['elapsed']]
metadata <- list(package=cfg$package, version=as.character(packageVersion(cfg$package)))
if (cfg$method == 'rfij') {
  forest <- ranger::ranger(x=X, y=y, num.trees=cfg$num_trees,
    min.node.size=cfg$min_node_size, replace=TRUE, sample.fraction=1,
    keep.inbag=TRUE, num.threads=1, seed=as.integer(cfg$seed))
  prediction <- predict(forest, Xq, type='se', se.method='infjack', num.threads=1)
  mu <- as.numeric(prediction$predictions)
  variance <- as.numeric(prediction$se)^2
  metadata$se_method <- 'infjack'
} else if (cfg$method == 'drf') {
  suppressPackageStartupMessages(library(Matrix))
  forest <- drf::drf(X=X, Y=matrix(y, ncol=1), num.trees=cfg$num_trees,
    ci.group.size=as.integer(cfg$num_trees/cfg$ci_groups),
    min.node.size=cfg$min_node_size, honesty=TRUE, sample.fraction=.5,
    num.features=cfg$num_features, splitting.rule='FourierMMD',
    response.scaling=TRUE, compute.oob.predictions=FALSE,
    num.threads=1, seed=as.integer(cfg$seed))
  prediction <- predict(forest, Xq, estimate.uncertainty=TRUE, num.threads=1)
  mu <- as.numeric(prediction$weights %*% y)
  stopifnot(max(abs(rowSums(prediction$weights)-1)) < 1e-7)
  group_means <- vapply(prediction$weights.uncertainty, function(w) {
    stopifnot(nrow(w)==cfg$ci_groups, max(abs(rowSums(w)-1)) < 1e-7)
    as.numeric(w %*% y)
  }, numeric(cfg$ci_groups))
  variance <- apply(group_means, 2, var)
  write.table(group_means, file.path(folder, 'group_means.csv'), sep=',',
              row.names=FALSE, col.names=FALSE)
  metadata$ci_groups <- cfg$ci_groups
  metadata$group_mean_matches_overall <- max(abs(colMeans(group_means)-mu))
  metadata$weighted_mean_exact <- TRUE
} else if (cfg$method == 'bart') {
  fit <- dbarts::bart(x.train=X, y.train=y, x.test=Xq,
    sigest=sd(y),
    ntree=cfg$num_trees, nskip=cfg$burn, ndpost=cfg$samples_per_chain,
    nchain=cfg$chains, nthread=1, combinechains=FALSE,
    k=cfg$k, base=cfg$tree_base, power=cfg$tree_power,
    sigdf=cfg$sigdf, sigquant=cfg$sigquant, keepevery=1,
    keeptrainfits=FALSE, keeptrees=FALSE, keepsampler=TRUE,
    verbose=FALSE, seed=as.integer(cfg$seed))
  samples <- fit$yhat.test
  stopifnot(identical(as.integer(dim(samples)),
                     as.integer(c(cfg$chains, cfg$samples_per_chain, nrow(Xq)))))
  diagnose <- function(samples) {
    # posterior expects iterations x chains x variables.
    a <- posterior::as_draws_array(aperm(samples, c(2,1,3)))
    s <- posterior::summarise_draws(a, "rhat", "ess_bulk", "ess_tail")
    list(max_rank_rhat=max(s$rhat), min_bulk_ess=min(s$ess_bulk),
         min_tail_ess=min(s$ess_tail),
         converged=all(is.finite(s$rhat)) && all(s$rhat<=cfg$max_rank_rhat) &&
           all(s$ess_bulk>=cfg$min_bulk_ess) && all(s$ess_tail>=cfg$min_tail_ess))
  }
  history <- list()
  draws_per_chain <- cfg$samples_per_chain
  for (round in 0:cfg$continuation_rounds) {
    diagnostics <- diagnose(samples)
    history[[length(history)+1]] <- c(list(round=round,
      samples_per_chain=draws_per_chain), diagnostics)
    jsonlite::write_json(history, file.path(folder, 'mcmc_progress.json'),
      auto_unbox=TRUE, digits=16, null='null')
    if (isTRUE(diagnostics$converged) || round==cfg$continuation_rounds) break
    draws_per_chain <- cfg$samples_per_chain*2^(round+1)
    fit$fit$startThreads(1L)
    continued <- fit$fit$run(numBurnIn=as.integer(cfg$burn*2^(round+1)),
                            numSamples=as.integer(draws_per_chain), updateState=FALSE)
    fit$fit$stopThreads()
    samples <- aperm(continued$test, c(3,2,1))
    stopifnot(identical(as.integer(dim(samples)),
                       as.integer(c(cfg$chains, draws_per_chain, nrow(Xq)))))
  }
  draws <- do.call(rbind, lapply(seq_len(cfg$chains), function(i) samples[i,,]))
  mu <- colMeans(draws)
  ci <- t(apply(draws, 2, quantile, probs=c(.025,.975), type=7))
  variance <- apply(draws, 2, var)
  writeBin(as.double(draws), file.path(folder, 'posterior_draws.bin'),
           size=8, endian='little')
  metadata <- c(metadata, diagnostics)
  metadata$mcmc_history <- history
  metadata$samples_per_chain <- draws_per_chain
  metadata$diagnostics_version <- as.character(packageVersion('posterior'))
  metadata$sigest <- fit$sigest
  metadata$draws_target <- 'latent regression function f; no future observation noise'
} else stop('Unknown method')
stopifnot(all(is.finite(mu)), all(is.finite(variance)), all(variance>=0))
if (cfg$method!='bart') {
  half <- qnorm(.975)*sqrt(variance)
  ci <- cbind(mu-half, mu+half)
}
write.csv(data.frame(mean=mu, lower=ci[,1], upper=ci[,2], variance=variance),
          file.path(folder, 'predictions.csv'), row.names=FALSE)
metadata$total_seconds <- proc.time()[['elapsed']]-started
jsonlite::write_json(metadata, file.path(folder, 'method_metadata.json'),
                    auto_unbox=TRUE, digits=16, null='null')
