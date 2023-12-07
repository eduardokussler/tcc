# TODO: YOU, THE USER, SHOULD CHANGE THESE TO YOUR DESIRED PATHS
export KOKKOS_SRC_DIR=`pwd`
export KOKKOS_INSTALL_DIR=$KOKKOS_SRC_DIR/build/install


mkdir build
cd build
/scratch/eekussler/cmake/cmake-3.28.0/bin/cmake \
  -D CMAKE_BUILD_TYPE="Release" \
  -D CMAKE_CXX_COMPILER=$KOKKOS_SRC_DIR/bin/nvcc_wrapper \
  -D CMAKE_INSTALL_PREFIX=$KOKKOS_INSTALL_DIR \
  -D Kokkos_ENABLE_SERIAL=ON \
  -D Kokkos_ENABLE_OPENMP=ON \
  -D Kokkos_ENABLE_CUDA=ON \
  -D Kokkos_ENABLE_CUDA_LAMBDA=ON \
  -D Kokkos_ARCH_PASCAL60=ON \
  \
  .. ;
make install
cd ../.. # Go back to top level dir 
