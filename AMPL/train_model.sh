#!/bin/bash

echo "hello"


echo $*


TRA="train_regression_model.py"

echo $TRA



curated_qmug=$1

echo $curated_qmug

odir=$2

final=$3

echo $odir
#best_model_dir='$odir''/best_models'

echo $*

#python3 -u $HPO -curated_qmug = $curated_qmug

python -u $TRA -curated_qmug $curated_qmug      \
               -odir $odir      \
               -final $final
     #          -best_model_dir $best_model_dir   \