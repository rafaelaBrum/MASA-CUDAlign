#!/bin/bash
echo " ----------------------------
   Updating package repositories
 ----------------------------"
sudo apt update
echo " ----------------------------
   Upgrading package repositories
 ----------------------------"
sudo apt upgrade -y
echo " ----------------------------
   Installing build-essential package
 ----------------------------"
sudo apt install build-essential -y
echo " ----------------------------
   Installing python package
 ----------------------------"
sudo apt install python -y
echo " ----------------------------
   Installing unzip (AWS Cli)
 ----------------------------"
sudo apt install unzip -y
if [ ! -f "awscliv2.zip" ]; then
    echo " ----------------------------
   Downloading AWS Cli install file
 ----------------------------"
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
fi
if [ ! -d "./aws/" ]; then
    echo " ----------------------------
   Unzipping AWS Cli install file
 ----------------------------"
    unzip awscliv2.zip
fi
echo " ----------------------------
   Installing AWS Cli
 ----------------------------"
sudo ./aws/install
aws configure
aws s3 ls
if [ ! -f "cuda_10.2.89_440.33.01_linux.run" ]; then
	echo " ----------------------------
   Downloading CUDA install file
 ----------------------------"
	wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run
fi

