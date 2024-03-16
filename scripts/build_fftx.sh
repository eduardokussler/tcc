export FFTX_HOME=`pwd`
shopt -s expand_aliases
alias cmake_new="/home/users/eekussler/cmake/bin/cmake"
mkdir work; cd ./work
git clone https://www.github.com/spiral-software/spiral-software

export SPIRAL_HOME=`pwd`/spiral-software

cd $SPIRAL_HOME/namespaces/packages
git clone https://www.github.com/spiral-software/spiral-package-fftx fftx
git clone https://www.github.com/spiral-software/spiral-package-simt simt
git clone https://www.github.com/spiral-software/spiral-package-mpi mpi

cd $SPIRAL_HOME
mkdir build; cd build
cmake_new ..
make install

cd $FFTX_HOME
cd src/library
./build-lib-code.sh CUDA	## build CUDA code
cd ../..
mkdir install
mkdir build; cd build
cmake_new -DCMAKE_INSTALL_PREFIX=$FFTX_HOME/install/fftx -DCMAKE_CUDA_COMPILER=/scratch/eekussler/kokkos/bin/nvcc_wrapper -D_codegen=CUDA ..     # build for CUDA, *or*
#cmake -DCMAKE_INSTALL_PREFIX=$FFTX_HOME/install/fftx -DCMAKE_CUDA_HOST_COMPILER=$(which gcc-9) -D_codegen=CUDA ..
make install
