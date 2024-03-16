export KOKKOS_SRC_DIR=/scratch/eekussler/kokkos
export KOKKOS_INSTALL_DIR=/scratch/eekussler/kokkos/build/install
export CABANA_INSTALL_DIR=/scratch/eekussler/Cabana/build/install

mkdir build
cd build
/scratch/eekussler/cmake/cmake-3.28.0/bin/cmake \
    -D CMAKE_BUILD_TYPE="Debug" \
    -D CMAKE_PREFIX_PATH=$KOKKOS_INSTALL_DIR \
    -D CMAKE_INSTALL_PREFIX=$CABANA_INSTALL_DIR \
    -D CMAKE_CXX_COMPILER=$KOKKOS_SRC_DIR/bin/nvcc_wrapper \
    -D Cabana_REQUIRE_CUDA=ON \
    .. ;
make -j 8 install
# -D Cabana_ENABLE_TESTING=ON

