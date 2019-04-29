# Edger-cleaner
Python script for cleaning EDGER data

## Clone repository
Clone the repository in your home directory.  
´´´console
git clone https://github.com/mikaelapisani/edger-cleaner.git
´´´

## Run in a virtualenv
´´´console
python3 -m venv edger-cleaner
source edger-cleaner/bin/activate
cd edger-cleaner 
pip install --upgrade pip
pip install -r requirements.txt
´´´
## Execution
For all years: python clean_edgar.py -c <config_path>    
For specific year: python clean_edgar.py -c <config_path> -y <year>    

## Execution in the TTU cluster
1. It is necessary to have installed conda. 
   Follow these guide if not installed: http://www.depts.ttu.edu/hpcc/userguides/application_guides/python.local_installation.php
2. Create virtualenv: 
´´´console
. $HOME/conda/etc/profile.d/conda.sh
conda activate
cd $HOME/edger-cleaner
pip install --upgrade pip
pip install -r requirements.txt
conda deactivate
´´´
3. Download the repository at your home directory
4. Edit config.properties file with the corresponding paths
4. Edit line 16 of mpi.sh file with the year you want to execute
5. Execute the following command:    
´´´console
qsub /home/mikleal/edger-cleaner/mpi/mpi.sh
´´´

### MPI
In order to run the jobs in the cluster it is used MPI. It can be found more information about how to run jobs in the cluster in the following link: http://www.depts.ttu.edu/hpcc/userguides/general_guides/job_submission.php.      
In this case it is configured only 1 process as it has to be serial.  In the future, the code could be modified in order to parallelize the process of the information and clean the data faster.   

## Configuration

Configure the file `config.properties`` as follows:         

´´´console
threshold=50
error_code_limit=300
output_size_mb=5000
access_token=
dropbox_folder=/EDGAR data 14-17/
dropbox_timeout=20000
rows_master_skip=11
data_path=/home/username/
master_path=/home/username/masters
results_path=/home/username/results
´´´

threshold:         Limit of firms for a given IP in a day, if this threshold is reached it is considered as robot
error_code_limit:  HTTP code from which rows are going to be removed 
output_size_mb:    limit size in MG for output files
access_token:      Dropbox access token   
dropbox_folder:    Dropbox folder name
dropbox_timeout:   Timeout for dropbox connection when uploading files   
rows_master_skip:  Amount of rows to skip in masters' file (comments)   
data_path:         Path for data, inside this folder there should be one folder per year     
master_path:       Path for masters' files   
results_path:      Path for temporary result files.       


## Data Cleaning
The process of cleaning the data consists in the following steps:  

1. Remove crawerls     
2. Remove index   
3. Remove codes >=error_code_limit   
4. Remove robots:  based on the number of unique firms that a given IP address downloads on a given day    
                   If it is more than the threshold is a robot   
5. Merge data with masters' data by cik and accession   

## Save data
The result data is saved in dropbox.     
As the files are going to be analyzed with SAS it is necessary that the size would be less than 5GB.   
In order to achieve these, for each day, it is checked if when appending the result for the day the size is greater than the threshold, in that case, the accummulated result is uploaded to dropbox and continue with the processing until there are no more files to process.   

It is necessary to create in dropbox an app to save the files into a folder. Generate a token for that app.
This token is the one that should be in the property access_token in the configuration.

## Columns from result
- ip: with ###.###.###.xxx – first three octets of the IP address with the fourth octet obfuscated with a 3 character string that preserves the uniqueness of the last octet without revealing the full identity of the IP
- date: apache log file date
- time: apache log file time
- cik: SEC central index key associated with the document requested
- accession: SEC document accession number associated with the document requested
- extention: document file type (e.g., html, txt, etc.)
- Form Type: submission type 
- Date Filed: date when the form was filed


    


