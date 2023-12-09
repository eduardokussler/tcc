export CABANA_INSTALL=../Cabana/build/install

cd ExaMPM
mkdir build
cd build
cmake \
  -D CMAKE_BUILD_TYPE="Debug" \
  -D CMAKE_PREFIX_PATH="$CABANA_INSTALL" \
  -D CMAKE_INSTALL_PREFIX=install \
  .. ;
make install