export FFTX_HOME=`pwd`
mkdir work; cd ./work
git clone https://www.github.com/spiral-software/spiral-software

export SPIRAL_HOME=`pwd`/spiral-software

cd $SPIRAL_HOME/namespaces/packages
git clone https://www.github.com/spiral-software/spiral-package-fftx fftx
git clone https://www.github.com/spiral-software/spiral-package-simt simt
git clone https://www.github.com/spiral-software/spiral-package-mpi mpi

cd $SPIRAL_HOME
mkdir build; cd build
cmake ..
make install

cd $FFTX_HOME
cd src/library
./build-lib-code.sh CUDA	## build CUDA code
cd ../..
mkdir install
mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX=$FFTX_HOME/install/fftx -D_codegen=CPU ..      # build for CPU, *or*
cmake -DCMAKE_INSTALL_PREFIX=$FFTX_HOME/install/fftx -D_codegen=CUDA ..     # build for CUDA, *or*
make install
