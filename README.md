# Edger-cleaner
Python script for cleaning EDGER data

## Virtualenv
python3 -m v

## Install requirements
source 
pip install --upgrade pip
pip install -r requirements.txt

## Execution

python3 clean_edgar.py -p '/Volumes/TOSHIBA EXT/rawEDGAR/' -r '/Users/mikaelapisanileal/Documents/SASUniversityEdition/myfolders' -y '2014'

## Cleaning
1. Remove crawerls
2. Remove index
3. Remove codes >=error_code_limit
4. Remove robots:  based on the number of unique firms that a given IP address downloads on a given day.
                   If it is more than the threshold is a robot.

## Columns from result
- ip:
- date:
- time:
- cik:
- accession:
- extention:
- Form Type:
- Date Filed:


    


