#!/usr/bin/bash

#SBATCH -t 10:00:00
#SBATCH --mem=20G
#SBATCH -o /hpc/hers_en/fsimoes/logs/log_%j.out   # %j gives job ID
#SBATCH -e /hpc/hers_en/fsimoes/logs/errlog_%j.out
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=francisconfqsimoes@gmail.com #Notifications will be sent.

if [[ -e $2 ]] # if the file exists.
then
	time $@ # run the file with the selected interpreter $1, and time it
else
	echo "$2 was not found."
fi
