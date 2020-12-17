#!/bin/bash
echo " ----------------------------
  Running tests
 ----------------------------"
cd tests_ebs/
COUNTER=1_$1
echo "Counter = $COUNTER"
echo " ----------------------------
  Test 1-3M
 ----------------------------"
cd 1-3M/
cudalign --blocks=512 --disk-size=1G --work-dir=teste_$COUNTER BA000035.2.fasta BX927147.1.fasta > saida_$COUNTER.txt
cd ../
echo " ----------------------------
  Test 2-5M
 ----------------------------"
cd 2-5M/
cudalign --blocks=512 --disk-size=3G --work-dir=teste_$COUNTER AE016879.1.fasta AE017225.1.fasta > saida_$COUNTER.txt
cd ../
echo " ----------------------------
  Test 3-7M
 ----------------------------"
cd 3-7M/
cudalign --blocks=512 --disk-size=3G --work-dir=teste_$COUNTER NC_005027.1.fasta NC_003997.3.fasta > saida_$COUNTER.txt
cd ../
echo " ----------------------------
  Test 4-10M
 ----------------------------"
cd 4-10M/
cudalign --blocks=512 --disk-size=5G --work-dir=teste_$COUNTER NC_017186.1.fasta NC_014318.1.fasta > saida_$COUNTER.txt
cd ../
echo " ----------------------------
  Test 5-23M
 ----------------------------"
cd 5-23M/
cudalign --blocks=512 --disk-size=10G --work-dir=teste_$COUNTER NT_033779.4.fasta NT_037436.3.fasta > saida_$COUNTER.txt
cd ../
