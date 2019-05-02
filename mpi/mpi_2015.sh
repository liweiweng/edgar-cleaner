#!/bin/sh
#$ -V
#$ -cwd
#$ -S /bin/bash
#$ -N MPI_EDGAR_2015
#$ -o $JOB_NAME.o$JOB_ID
#$ -e $JOB_NAME.e$JOB_ID
#$ -q omni
#$ -pe sm 1
#$ -l h_vmem=5.3G
#$ -l h_rt=48:00:00
#$ -P quanah

module load intel impi

mpirun --machinefile machinefile.$JOB_ID -np 1 sh /home/mikleal/edger-cleaner/mpi/run.sh 2015
