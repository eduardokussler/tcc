export OMPI_CXX=/scratch/eekussler/kokkos/bin/nvcc_wrapper
export CUDA_PATH=/usr/local/cuda-12.3/
#change kokkos path on makefile
make -j KOKKOS_ARCH=SNB,Pascal60 KOKKOS_DEVICES=Cuda CXX=nvcc MPI=0
