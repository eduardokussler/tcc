#!/bin/bash
mkdir install
autoreconf -i
./configure --prefix=`pwd`/install
make
make check
make install

cd Examples/3D/NavierStokes3D/RisingThermalBubble_Config1_CUDA
gcc -o setup aux/init_parallel.c -lm
./setup

cd ../DNS_IsotropicTurbulenceDecay_CUDA
gcc -o setup_fourier aux/fourier.c  -lm -lfftw3
./read_output_fourier
gcc -o setup_kinectic aux/kineticenergy.c  -lm -lfftw3
./setup_kinectic
gcc -o setup aux/init.c  -lm -lfftw3
./setup 
