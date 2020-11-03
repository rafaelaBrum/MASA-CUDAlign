#!/bin/bash
if [ -z "$1" ]; then
    echo "CUDA arch needed"
    exit 1
fi
if [ ! -d "MASA-CUDAlign/" ]; then
    echo " ----------------------------
  Cloning repository
 ----------------------------"
    git clone https://github.com/rafaelaBrum/MASA-CUDAlign.git
fi
if [ ! -f "MASA-CUDAlign/cudalign" ]; then
    echo " ----------------------------
  Compiling MASA-CUDAlign
 ----------------------------"
    cd MASA-CUDAlign/masa-cudalign-3.9.1.1024
    ./configure -with-cuda-arch=$1
    make
    ./cudalign --list-gpus
    cd ~/
fi
echo " ----------------------------
  Updating PATH env variables
 ----------------------------"
export PATH=$PATH:/home/ubuntu/MASA-CUDAlign/masa-cudalign-3.9.1.1024
