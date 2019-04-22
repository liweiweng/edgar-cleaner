#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isdir, join
import re
import sys
import getopt
import math
import datetime
import dropbox
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

threshold = 50
error_code_limit = 300
output_size_gb = 5*10000000000
access_token = "dhZNW6DTN2AAAAAAAAAC2ebJv8jOEPyPNb31b0cf7EtbeVqq8YpRPmiKjLxVT099"
dropbox_folder = "/edgar_test/"

#Transfer data to dropbox
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)


#function to process one file
#data cleaning process
    #   remove crawerls
    #   remove index
    #   remove codes >=error_code_limit
    #   remove robots:  based on the number of unique firms that a given IP address
    #                   downloads on a given day. if it is more than the threshold is a robot.
    #
    # columns to keep:ip,date,time,cik,accession(mapping with form type and date),extention         
def process_day(path, date_dir, day_file):
    path_day = path + date_dir + '/' + day_file
    zf = zipfile.ZipFile(path_day)
    zp_list = zipfile.ZipFile.namelist(zf)
    csv_regex = re.compile('(.*)\.csv')
    df = pd.DataFrame(data={})
    for file in zp_list:
        matcher = csv_regex.match(file)
        if (matcher):
            df = pd.read_csv(zf.open(file))
            # df = pd.read_csv(zf.open(file), dtype={'ip':str, 'date':str, 'time':str, 'zone':str, 'cik':str, 'accession':str, 'extention':str, 'code':str,
       #'size':str, 'idx':str, 'norefer':str, 'noagent':str, 'find':str, 'crawler':str, 'browser':str})
            print("Processing day: " + file)
            print("original size:" + str(df.size))
            
            df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < error_code_limit)]
            df = df[['ip', 'date', 'time', 'cik', 'accession', 'extention']]
            print("after removeing crawerls, index, codes:" + str(df.size))
            
            downloads_count = df.ip.value_counts()
            downloads_count = downloads_count[downloads_count<threshold].index
            df = df[df.ip.isin(downloads_count)]
            print("after removing robots:" + str(df.size))
    return df
 
#save data into csv of chunk size defined (GB)         
def save_csv(df, results_path, year):
    row_size = sum([df.memory_usage()[1] for pair in df.memory_usage().iteritems()])
    chunks = math.trunc(row_size/output_size_gb)
    transferData = TransferData(access_token)
    if chunks>0:
        idx = 0
        for chunk in np.array_split(df, chunks):
            file_from = results_path + '/' + year + '_' + str(idx) + '.csv'
            file_to = dropbox_folder + year + '_' + str(idx) + '.csv'
            chunk.to_csv(file_from, index=False)
            transferData.upload_file(file_from, file_to)
            os.remove(file_from)
            idx=+1
    else:
        file_from = results_path + '/' + year + '_0.csv'
        file_to = dropbox_folder + year + '_0.csv'
        df.to_csv(file_from, index=False)
        transferData.upload_file(file_from, file_to)
        os.remove(file_from)


#load data from master files and clean it
def load_master(master_path, year):
    masters = pd.DataFrame(data={})
    regex_file = re.compile('master' + year + '.*')
   
    for master_file in listdir(master_path):
        if (regex_file.match(master_file)):
            master = pd.read_csv(master_path + master_file, skiprows=11,
                names=['CIK','Company Name', 'Form Type', 'Date Filed', 'Filename'],
                sep='|')
            masters = masters.append(master)
    
    #modify filename data to keep accession number
    masters['Filename'] = masters['Filename'].apply(lambda x: x.split('/')[3].replace('.txt', ''))
    #keep columns of interest
    masters = masters[['Filename', 'CIK', 'Form Type','Date Filed']]
    return masters

 
def process_year(path, master_path, results_path, year):
    df = pd.DataFrame(data={})
    regex_zip = re.compile('log([0-9]{4})([0-9]{2})([0-9]{2}).zip')
    for day_file in listdir(path + year):
        if regex_zip.match(day_file):
            df = df.append(process_day(path, year, day_file))          
    masters = load_master(master_path, year)
    data_merged = pd.merge(df, masters, how='inner', left_on=['accession', 'cik'], 
                           right_on=['Filename', 'CIK'])
    data_merged = data_merged[['ip', 'date', 'time', 'cik', 'accession', 
                               'extention', 'Form Type','Date Filed']]
    save_csv(data_merged, results_path, year)

#for each date folder, process days files and append into one dataframe
#save data into csv files
def process_data(path, master_path, results_path):
    date_dirs = [f for f in listdir(path) if isdir(join(path, f))]
    regex_dir = re.compile('([0-9]{4})')
    for year in date_dirs:
        if (regex_dir.match(year)):
            before = datetime.datetime.now()
            process_year(path, master_path, year)
            after = datetime.datetime.now()
            print('time elapsed for ' + year + ':' + str(after-before))
           

def info():
    print('clean_edgar.py -p <path> -r <results_path>')

def main(argv):
   path = ''
   master_path = ''
   results = ''
   year = ''
   try:
      opts, args = getopt.getopt(argv,'hp:m:r:y:',['path=','master=','results=', 'year='])
   except getopt.GetoptError:
      info()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-p', '--path'):
         path = arg
      elif opt in ('-m', '--master'):
         master_path = arg
      elif opt in ('-r', '--results'):
         results = arg
      elif opt in ('-y', '--year'):
         year = arg
   if (year==''):
       process_data(path, master_path, results)
   else:
       process_year(path, master_path, results, year)
   
if __name__ == "__main__":
    main(sys.argv[1:])

#python clean_edgar.py -p '/Volumes/TOSHIBA EXT/rawEDGAR/' -m '/Volumes/TOSHIBA EXT/master index files/' -r '/Users/mikaelapisanileal/Documents/SASUniversityEdition/myfolders' -y '2014'