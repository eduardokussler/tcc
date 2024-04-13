#!/bin/bash
mkdir install
autoreconf -i
./configure --prefix=`pwd`/install
make
make check
make install