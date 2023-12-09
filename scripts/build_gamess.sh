#!/bin/bash
source source_me_OLCF 
NMPI=0
EXEC=rimp2-cublas rimp2-cublasxt rimp2-nvblas
./run_after_rebuild.sh