# TODO: YOU, THE USER, SHOULD CHANGE THESE TO YOUR DESIRED PATHS
export KOKKOS_SRC_DIR=`pwd`
export KOKKOS_INSTALL_DIR=$KOKKOS_SRC_DIR/build/install
shopt -s expand_aliases
alias cmake_new="/home/users/eekussler/cmake/bin/cmake"
mkdir build
cd build
cmake_new  \
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
