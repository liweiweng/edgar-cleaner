#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import pandas as pd
import zipfile
import numpy as np
from os import listdir
from os.path import isdir, join
import re
import sys
import getopt
import math


threshold = 50
error_code_limit = 300
output_size_gb = 5*10000000000

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
            print("Processing day: " + file)
            print("original size:" + str(df.size))
            
            df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < error_code_limit)]
            df.drop(columns=['zone','code','size','idx','norefer','noagent','find','crawler','browser'], inplace=True)
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
    if chunks>0:
        idx = 0
        for chunk in np.array_split(df, chunks):
            chunk.to_csv(results_path + '/' + year + '_' + str(idx) + '.csv', index=False)
            idx=+1
    else:
        df.to_csv(results_path + '/' + year + '_0.csv', index=False)


#load data from master files and clean it
def load_master(master_path, year):
    master_path = '/Volumes/TOSHIBA EXT/master index files/'
    year = '2014'
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

#for each date folder, process days files and append into one dataframe
#save data into csv files
def process_data(path):
    date_dirs = [f for f in listdir(path) if isdir(join(path, f))]
    regex_dir = re.compile('([0-9]{4})')
    regex_zip = re.compile('log([0-9]{4})([0-9]{2})([0-9]{2}).zip')
    for year in date_dirs:
        if (regex_dir.match(year)):
            df = pd.DataFrame(data={})
            for day_file in listdir(path + year):
                if regex_zip.match(day_file):
                       df = df.append(process_day(path, year, day_file))
    return df
            
def process_year(path, results_path, year):          
    masters = load_master(path, year)
    df = process_data('/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/')
    data_merged = pd.merge(df, masters, how='inner', left_on=['accession', 'cik'], 
                           right_on=['Filename', 'CIK'])
    data_merged = data_merged[['ip', 'date', 'time', 'cik', 'accession', 
                               'extention', 'Form Type','Date Filed']]
    save_csv(data_merged, results_path, year)

def main(argv):
    
   path = ''
   results = ''
   try:
      opts, args = getopt.getopt(argv,'hp:r:',['path=','results='])
   except getopt.GetoptError:
      print ('clean_edgar.py -p <path> -r <results_path>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('clean_edgar.py -p <path> -r <results_path>')
         sys.exit()
      elif opt in ('-p', '--path'):
         path = arg
      elif opt in ('-r', '--results'):
         results = arg
       
   process_data(path, results)
   
if __name__ == "__main__":
    main(sys.argv[1:])

#python clean_edgar.py -p '/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/' -r '/Users/mikaelapisanileal/Documents/SASUniversityEdition/myfolders'