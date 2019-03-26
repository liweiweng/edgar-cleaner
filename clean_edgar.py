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

threshold = 50
error_code_limit = 300

#function to process one file
def process_day(path):
    zf = zipfile.ZipFile(path)
    #TODO: validate there is csv file inside 
    df = pd.read_csv(zf.open(zipfile.ZipFile.namelist(zf)[0])) 
    
    #data cleaning process
    #   remove crawerls
    #   remove index
    #   remove codes >=error_code_limit
    print("original size:" + str(df.size))
    df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < error_code_limit)]
    print("new size:" + str(df.size))
    
    #remove robots:  based on the number of unique firms that a given IP address
    #downloads on a given day. if it is more than the threshold is a robot.
    downloads_count = df.ip.value_counts()
    d = downloads_count[downloads_count<threshold].index
    df = df[df.ip.isin(d)]
    print("new size:" + str(df.size))


def process_data(path):
    date_dirs = [f for f in listdir(path) if isdir(join(path, f))]
    regex_dir = re.compile('([0-9]{4})')
    regex_zip = re.compile('log([0-9]{4})([0-9]{2})([0-9]{2}).zip')
    for date_dir in date_dirs:
        if (regex_dir.match(date_dir)):
            for day_file in listdir(path + date_dir):
                if regex_zip.match(day_file):
                       process_day(path + date_dir + '/' + day_file)
       
 


process_data('/Users/mikaelapisanileal/Desktop/edgar/edger-cleaner/')


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

