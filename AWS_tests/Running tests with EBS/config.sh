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
fi
