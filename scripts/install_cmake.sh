wget https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3.tar.gz

sudo apt install libssl3 libssl-dev

mkdir build_cmake
cd build_cmake
tar -xvf ../cmake-3.28.3.tar.gz
cd cmake-3.28.3
./bootstrap && make -j 6 && sudo make install