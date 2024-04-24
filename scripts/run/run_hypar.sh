#!/bin/bash

cd ../../projetos/hypar/install/bin
HYPAR_HOME=$(pwd)

echo "Change parameters to solver.inp files"
echo "iproc must match the mpi ranks"

EXAMPLES=(/Examples/3D/NavierStokes3D/RisingThermalBubble_Config1_CUDA /Examples/3D/NavierStokes3D/DNS_IsotropicTurbulenceDecay_CUDA )

for example in ${EXAMPLES[@]}
do
    cd $HYPAR_HOME/../../$example
    $HYPAR_HOME/HyPar
done