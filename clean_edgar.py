#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import pandas as pd
import zipfile
import numpy as np

#process information for one day
#load data into dataframe

year_data = '2014'
month_data = '01'
day_data = '01'

#TODO: receive as paramter the path
path = '/Users/mikaelapisanileal/Desktop/edgar/'
log_path = path + year_data + '/log' + year_data + month_data + day_data + '.zip'

zf = zipfile.ZipFile(log_path)
#TODO: validate there is csv file inside 
df = pd.read_csv(zf.open(zipfile.ZipFile.namelist(zf)[0])) 

#data cleaning process
#   remove crawerls
#   remove index
#   remove codes >=300
print("original size:" + str(df.size))
df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < 300)]
print("new size:" + str(df.size))

#TODO: remove robots