#!/bin/bash

mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` ..
make -j 8