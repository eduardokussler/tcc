mkdir build
cd build

KOKKOS_SRC_DIR=/scratch/eekussler/kokkos
CABANA_INSTALL_DIR=/scratch/eekussler/Cabana/build/install

cmake -DCMAKE_PREFIX_PATH=$CABANA_INSTALL_DIR -DCMAKE_CXX_COMPILER=$KOKKOS_SRC_DIR/bin/nvcc_wrapper ..

make VERBOSE=1