#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import pandas as pd
import zipfile
import numpy as np
import os
from os import listdir
from os.path import isdir, join
import re

threshold = 50
error_code_limit = 300

#function to process one file
#data cleaning process
    #   remove crawerls
    #   remove index
    #   remove codes >=error_code_limit
    #   remove robots:  based on the number of unique firms that a given IP address
    #                   downloads on a given day. if it is more than the threshold is a robot.
          
def process_day(path, date_dir, day_file, results_path):
    path_day = path + date_dir + '/' + day_file
    zf = zipfile.ZipFile(path_day)
    zp_list = zipfile.ZipFile.namelist(zf)
    csv_regex = re.compile('(.*)\.csv')
    result_dir = results_path + '/' + date_dir
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    for file in zp_list:
        matcher = csv_regex.match(file)
        if (matcher):
            df = pd.read_csv(zf.open(file))
            print("Processing day: " + file)
            print("original size:" + str(df.size))
            
            df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < error_code_limit)]
            df.drop(columns=['crawler'])
            print(df.head())
            print("after removeing crawerls, index, codes:" + str(df.size))
            
            downloads_count = df.ip.value_counts()
            d = downloads_count[downloads_count<threshold].index
            df = df[df.ip.isin(d)]
            print("after removing robots:" + str(df.size))
            df.to_csv(result_dir + '/' + matcher.group(1) + '.csv.gzip', compression='gzip', index=False)
            


def process_data(path, results_path):
    date_dirs = [f for f in listdir(path) if isdir(join(path, f))]
    regex_dir = re.compile('([0-9]{4})')
    regex_zip = re.compile('log([0-9]{4})([0-9]{2})([0-9]{2}).zip')
    for date_dir in date_dirs:
        if (regex_dir.match(date_dir)):
            for day_file in listdir(path + date_dir):
                if regex_zip.match(day_file):
                       process_day(path, date_dir, day_file, results_path)


#process_data('/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/', '/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/results')

#process_day('/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/', '2014', 'log20140101.zip', '/Users/mikaelapisanileal/Documents/edgar/edger-cleaner/results')


def main(argv):
    
   path = ''
   try:
      opts, args = getopt.getopt(argv,"hp",["path="])
   except getopt.GetoptError:
      print ('clean_edgar.py -p <path>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('clean_edgar.py -p <path>')
         sys.exit()
      elif opt in ("-p", "--path"):
         path = arg
       
    process_data(path)
   
if __name__ == "__main__":
    main(sys.argv[1:])

