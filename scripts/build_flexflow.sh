#!/bin/bash
# Set this variables on the config.linux file
FF_GPU_BACKEND=cuda
FF_CUDA_ARCH=80 #autodetect 
FF_BUILD_ALL_EXAMPLES=On

mkdir build
cd build
../config/config.linux
make -j 4