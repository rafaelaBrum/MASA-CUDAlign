#!/bin/bash
if [ -z "$1" ]; then
    echo "CUDA arch needed"
	echo " ----------------------------
   Installing CUDA driver e toolkit (10.2)
 ----------------------------"
	sudo sh cuda_10.2.89_440.33.01_linux.run --silent
	echo " ----------------------------
  Updating LD_LIBRARY_PATH and PATH env variables to see CUDA libraries
 ----------------------------"
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64
	export PATH=$PATH:/usr/local/cuda-10.2/bin
else
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
  Updating PATH env variables to see cudalign
 ----------------------------"
  export PATH=$PATH:/home/ubuntu/MASA-CUDAlign/masa-cudalign-3.9.1.1024
  if [ ! -d "tests/" ]; then
    mkdir tests
    s3fs rafaela-masa-cudalign tests/
fi
cd tests/

fi
