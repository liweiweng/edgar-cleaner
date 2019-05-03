#!/bin/bash

. $HOME/conda/etc/profile.d/conda.sh
conda activate
if [[ $# -eq 1 ]]; then
   YEAR=$1
   python $HOME/edgar-cleaner/clean_edgar.py -c $HOME/edgar-cleaner/config.properties -y $YEAR
else
   python $HOME/edgar-cleaner/clean_edgar.py -c $HOME/edgar-cleaner/mpi/config.properties
fi

