#!/bin/bash
export OMPI_CXX=/home/eekussler/tcc/projetos/dependencies/kokkos/bin/nvcc_wrapper
export CUDA_PATH=/usr/local/cuda-11.7/
make clean
make -j 1 KOKKOS_ARCH=SNB,Pascal60 KOKKOS_DEVICES=Cuda CXX=$OMPI_CXX MPI=0
