export OMPI_CXX=/scratch/eekussler/kokkos/bin/nvcc_wrapper
make -j KOKKOS_ARCH=SNB,Pascal60 KOKKOS_DEVICES=Cuda CXX=nvcc MPI=0
