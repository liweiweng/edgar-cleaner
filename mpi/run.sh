#!/bin/bash

. $HOME/conda/etc/profile.d/conda.sh
conda activate
if [[ $# -eq 1 ]]; then
   YEAR=$1
   python /home/mikleal/edger-cleaner/clean_edgar.py -c $HOME/edger-cleaner/config.properties -y $YEAR
else
   python /home/mikleal/edger-cleaner/mpi/clean_edgar.py -c $HOME/edger-cleaner/mpi/config.properties
fi

