export CABANA_INSTALL_DIR=/scratch/eekussler/Cabana/build/install


cd ExaMPM
mkdir build
cd build
cmake \
  -D CMAKE_BUILD_TYPE="Debug" \
  -D CMAKE_PREFIX_PATH="$CABANA_INSTALL_DIR" \
  -D CMAKE_INSTALL_PREFIX=install \
  .. ;
make install