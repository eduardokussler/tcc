#!/bin/bash
tests=("rush_larsen_gpu_cuda" "rush_larsen_gpu_lambda_cuda")

#on my laptop, needed to override host compiler on each test makefile 


iterations=$1 #self explanatory
gbs=$2 #gb used by kernel
if [ -z $iterations ]; then
    iterations=100000
fi

if [ -z $gbs ]; then
    gbs=3
fi

goulash_home=`pwd`

for test in ${tests[@]}; do
    echo $test
    cd tests/rush_larsen/$test
    make
    ./$test  $iterations  $gbs
    cd $goulash_home
done
