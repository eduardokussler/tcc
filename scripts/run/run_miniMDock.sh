
#!/bin/bash

INPUT_PREFIX=./input/
TESTS=(7cpa/7cpa_ligand.pdbqt  nsc1620/NSC1620.pdbqt)
EXECUTABLE=./bin/autodock_gpu_64wi
cd ../../projetos/miniMDock/

for test in ${TESTS[@]}
do
    echo "running test $test"
    $EXECUTABLE -lfile $INPUT_PREFIX$test -nrun 10
done