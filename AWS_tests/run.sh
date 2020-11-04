#!/bin/bash
echo " ----------------------------
  Running tests
 ----------------------------"
if [ ! -d "testes/" ]; then
    echo " ----------------------------
   Creating tests root folder
 ----------------------------"
    mkdir tests
fi
cd tests/
echo " ----------------------------
  Test 1-3M
 ----------------------------"
if [ ! -d "1-3M/" ]; then
    echo " ----------------------------
   Copying files from s3
 ----------------------------"
    mkdir 1-3M
    aws s3 cp s3://rafaela-masa-cudalign/1-3M.zip
    unzip 1-3M.zip -d 1-3M/ 
fi
cd 1-3M/
COUNTER=1
while [  $COUNTER -lt 4 ]; do
	echo "Counter = $COUNTER"
	COUNTER=$((COUNTER+1))
  cudalign --blocks=512 --disk-size=1G --work-dir=teste_$COUNTER BA000035.2.fasta BX927147.1.fasta
done
cd ../
echo " ----------------------------
  Test 2-5M
 ----------------------------"
if [ ! -d "2-5M/" ]; then
    echo " ----------------------------
   Copying files from s3
 ----------------------------"
    mkdir 2-5M
    aws s3 cp s3://rafaela-masa-cudalign/2-5M.zip
    unzip 2-5M.zip -d 2-5M/
fi
cd 2-5M/
COUNTER=1
while [  $COUNTER -lt 4 ]; do
	echo "Counter = $COUNTER"
	COUNTER=$((COUNTER+1))
  cudalign --blocks=512 --disk-size=3G --work-dir=teste_$COUNTER AE016879.1.fasta AE017225.1.fasta
done
cd ../
echo " ----------------------------
  Test 3-7M
 ----------------------------"
if [ ! -d "3-7M/" ]; then
    echo " ----------------------------
   Copying files from s3
 ----------------------------"
    mkdir 3-5M
    aws s3 cp s3://rafaela-masa-cudalign/3-5M.zip
    unzip 3-5M.zip -d 3-5M/
fi
cd 3-7M/
COUNTER=1
while [  $COUNTER -lt 4 ]; do
	echo "Counter = $COUNTER"
	COUNTER=$((COUNTER+1))
  cudalign --blocks=512 --disk-size=3G --work-dir=teste_$COUNTER NC_005027.1.fasta NC_003997.3.fasta
done
cd ../
echo " ----------------------------
  Test 4-10M
 ----------------------------"
if [ ! -d "4-10M/" ]; then
    echo " ----------------------------
   Copying files from s3
 ----------------------------"
    mkdir 4-10M
    aws s3 cp s3://rafaela-masa-cudalign/4-10M.zip
    unzip 4-10M.zip -d 4-10M/
fi
cd 4-10M/
COUNTER=1
while [  $COUNTER -lt 4 ]; do
	echo "Counter = $COUNTER"
	COUNTER=$((COUNTER+1))
  cudalign --blocks=512 --disk-size=5G --work-dir=teste_$COUNTER NC_017186.1.fasta NC_014318.1.fasta
done
cd ../
echo " ----------------------------
  Test 5-23M
 ----------------------------"
if [ ! -d "5-23M/" ]; then
    echo " ----------------------------
   Copying files from s3
 ----------------------------"
    mkdir 5-23M
    aws s3 cp s3://rafaela-masa-cudalign/5-23M.zip
    unzip 5-23M.zip -d 5-23M/
fi
cd 5-23M/
COUNTER=1
while [  $COUNTER -lt 4 ]; do
	echo "Counter = $COUNTER"
	COUNTER=$((COUNTER+1))
  cudalign --blocks=512 --disk-size=10G --work-dir=teste_$COUNTER NT_033779.4.fasta NT_037436.3.fasta
done
cd ../
