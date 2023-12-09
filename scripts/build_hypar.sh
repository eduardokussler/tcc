#!/bin/bash
mkdir install
autoconf ./configure.ac
./configure --prefix=`pwd`/install
make
make check
make install