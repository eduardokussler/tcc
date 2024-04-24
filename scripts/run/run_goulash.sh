#!/bin/bash

tests=("rush_larsen_gpu_cuda" "rush_larsen_gpu_lambda_cuda")

cd ../../projetos/goulash/



iterations=$1 #self explanatory
gbs=$2 #gb used by kernel
if [ -z $iterations ]; then
    iterations=500
fi

if [ -z $gbs ]; then
    gbs=8
fi

goulash_home=`pwd`

for test in ${tests[@]}; do
    echo $test
    cd tests/rush_larsen/$test
    ./$test  $iterations  $gbs
    cd $goulash_home
done
