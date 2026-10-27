args <- commandArgs(trailingOnly=TRUE)
out <- args[1]
suppressPackageStartupMessages(library(RLT))
suppressPackageStartupMessages(library(jsonlite))
cfg <- fromJSON(file.path(out,'config.json'))
X <- as.matrix(read.csv(file.path(out,'X.csv'),check.names=FALSE))
Xq <- as.matrix(read.csv(file.path(out,'Xq.csv'),check.names=FALSE))
y <- read.csv(file.path(out,'y.csv'))[[1]]
attempts <- list()
for (trees in cfg$trees_schedule) {
  fit <- RLT(X,y,model='regression',reinforcement=FALSE,ntrees=trees,
             mtry=max(1,as.integer(ncol(X)/2)),nmin=cfg$nmin,
             resample.replace=FALSE,resample.prob=.5,var.mode='matched',
             importance='distribute',ncores=1,verbose=0,seed=cfg$seed)
  pred <- predict(fit,testx=Xq,var.est=TRUE,ncores=1)
  good <- is.finite(pred$Variance) & pred$Variance>=0 & is.finite(pred$Prediction)
  attempts[[length(attempts)+1]] <- list(trees=trees,invalid_queries=sum(!good))
  write_json(attempts,file.path(out,'variance_attempts.json'),auto_unbox=TRUE,pretty=TRUE)
  if(all(good)) break
  rm(fit);gc()
}
if(!all(good)) stop('RF-U sampling variance remains invalid; no clipping or omitted queries allowed')
half <- qnorm(.975)*sqrt(pred$Variance)
write.csv(data.frame(mean=pred$Prediction,variance=pred$Variance,
                     lower=pred$Prediction-half,upper=pred$Prediction+half),
          file.path(out,'predictions.csv'),row.names=FALSE)
write_json(list(package_version=as.character(packageVersion('RLT')),
                R_version=R.version.string,trees=trees,variance_mode='matched',
                attempts=attempts),file.path(out,'method_metadata.json'),auto_unbox=TRUE,pretty=TRUE)
