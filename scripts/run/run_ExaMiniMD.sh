#!/bin/bash

make -j KOKKOS_ARCH=SNB,Pascal60 KOKKOS_DEVICES=Cuda CXX=nvcc MPI=0