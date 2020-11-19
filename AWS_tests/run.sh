#!/bin/bash
USAGE="Usage: run.sh B D work_dir first_filename second_filename \n\
	where \n\
	B is the number of CUDA blocks MASA-CUDAlign will run \n\
	D is the size of disk to be used for storing special rows (needs to end with a M or a G) \n\
	work_dir is the folder where the results and special rows will be saved \n\ 
	sequence1 and sequence2 are the FASTA files with the sequences to be aligned \n\
	OPTIONAL ARGS: \n\
	first_filename will be the output_file, where the program output will be printed \n\
	second_filename will be the error_file, where the stderr will be printed"
#checking if the script has the needed args
if [[ $# -gt 3 ]]; then
    echo "Script needs at least 5 arguments."
	echo $USAGE
	exit 1
fi
OPTIONS=''
#checking if the first arg is a number (# blocks)
re='^[0-9]+$'
if ! [[ $1 =~ $re ]]; then
    echo "First arg needs to be a number."
    echo $USAGE		
    exit 1
else
    OPTIONS='${OPTIONS} --blocks=${1}'
fi
#checking the format of the second arg (disk size)
re='^[0-9]+[G-M]$'
if ! [[ $2 =~ $re ]]; then
    echo "Second arg needs to be a number followed by a M or a G (ex. 1G)"
	echo $USAGE
	exit 1
else
	OPTIONS='${OPTIONS] --disk-size=${2}'
fi 
#adding third arg (work_dir) into the OPTIONS string
OPTIONS='${OPTIONS} --work-dir=${3}'
#adding the FASTA files from current directory
FILENAMES='ls ./*.fasta'
for file in $FILENAMES
	echo 'file= ${file}'
	OPTIONS='${OPTIONS} ${file}'
fi
#checking if there is the name of the first file (to be the output_file)
if [[ -z $4 ]]; then
	OPTIONS='${OPTIONS} > ${6}'
	#checking if there is the name of the second file (to be the error_file)
	if [[ -z $5 ]]; then
		OPTIONS='${OPTIONS} 2> ${7}'
fi
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64
export PATH=$PATH:/usr/local/cuda-10.2/bin:/home/ubuntu/MASA-CUDAlign/masa-cudalign-3.9.1.1024
cudalign $OPTIONS 