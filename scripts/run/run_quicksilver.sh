#!/bin/bash


# Alter /Examples/AllEscape/allEscape.inp
# nParticles: 900000
#  nSteps: 2000
cd ../../projetos/Quicksilver/src


TESTS=(../Examples/CORAL2_Benchmark/Problem1/Coral2_P1_1.inp
       ../Examples/CORAL2_Benchmark/Problem1/Coral2_P1_4096.inp 
       ../Examples/CORAL2_Benchmark/Problem2/Coral2_P2_1.inp 
       ../Examples/CORAL2_Benchmark/Problem2/Coral2_P2_4096.inp
       ../Examples/Homogeneous/homogeneousProblem_v3_wq.inp)


for TEST in ${TESTS[@]}
do
    ./qs --inputFile $TEST #--nSteps 2000 --nParticles 900000
done