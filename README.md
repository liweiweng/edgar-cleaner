# Edger-cleaner
Python script for cleaning EDGER data

## Clone repository
git clone https://github.com/mikaelapisani/edger-cleaner.git

## Run in a virtualenv
´´´console
python3 -m venv edger-cleaner
source edger-cleaner/bin/activate
cd edger-cleaner 
pip install --upgrade pip
pip install -r requirements.txt
´´´
## Execution
For all years: nohup python3 clean_edgar.py -p <folders_path> -r <results_path> &
For specific year: nohup python3 clean_edgar.py -p <folders_path> -r <results_path> -y <year> &

## Execution in the TTU cluster
1. It is necessary to have installed conda. 
   Follow these guide if not installed: http://www.depts.ttu.edu/hpcc/userguides/application_guides/python.local_installation.php
2. Create virtualenv: 
´´´console
. $HOME/conda/etc/profile.d/conda.sh
conda activate
cd edger-cleaner
pip install --upgrade pip
pip install -r requirements.txt
conda deactivate
´´´
3. Run script:

The files to process are in separate folders by years in the home directory.  

´´´console
mkdir $HOME/results
conda activate
nohup python3 clean_edgar.py -p '$HOME' -r '$HOME/results' -y '2014' &
´´´
## Data Cleaning
The process of cleaning data consists in the following steps:  

1. Remove crawerls
2. Remove index
3. Remove codes >=error_code_limit
4. Remove robots:  based on the number of unique firms that a given IP address downloads on a given day.
                   If it is more than the threshold is a robot.
5. Merge data with masters' data by cik and accession.

## Save data
The result data is saved in dropbox.
As the files are going to be analyzed with SAS it is necessary that the size would be less than 5GB.   
In order to achieve these, for each day, it is checked if when appending the result for the day the size is greater than the threshold, in that case, the accummulated result is uploaded to dropbox and continue with the processing until there are no more files to process.   

## Columns from result
- ip: with ###.###.###.xxx – first three octets of the IP address with the fourth octet obfuscated with a 3 character string that preserves the uniqueness of the last octet without revealing the full identity of the IP
- date: apache log file date
- time: apache log file time
- cik: SEC central index key associated with the document requested
- accession: SEC document accession number associated with the document requested
- extention: document file type (e.g., html, txt, etc.)
- Form Type: submission type 
- Date Filed: date when the form was filed


    


