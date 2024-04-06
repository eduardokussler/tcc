#/bin/bash

# Set these on the GNUMakefile for each tutorial example you want to use
AMREX_HOME=../projetos/dependencies/amrex/
AMREX_HYDRO_HOME=../projetos/dependencies/AMReX-Hydro/
USE_CUDA=TRUE # -> Set USE_OMP to FALSE
COMP=gnu
# Then, just use make

TUTORIALS_PATH=../projetos/IAMR/Tutorials

cd $TUTORIALS_PATH
pwd

shopt -s nullglob
shopt -s dotglob

EXAMPLES=(*/)


for test in ${EXAMPLES[@]}; do
    echo $test
    cd $test
    make -j 8
    cd ..
done