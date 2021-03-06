#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:37:40 2019

@author: mikaelapisanileal
"""

import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isdir, join
import re
import math
import sys
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile
    
from transfer import TransferData
import logging

#Class for processing, cleaning and merging the EDGAR data
class Processor:
    def __init__(self, conf):
        self.config = conf
        self.transferData = TransferData(self.config.access_token, 
                                         self.config.dropbox_chunck, 
                                         self.config.dropbox_timeout)
        #set logging configuration
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.getLevelName(self.config.log_level))
        self.logging = logging.getLogger()        
      
    #function to process one file (a day)
    #data cleaning process
        #   remove crawerls
        #   remove index
        #   remove codes >=error_code_limit
        #   remove robots:  based on the number of unique firms that a given IP address
        #                   downloads on a given day. if it is more than the threshold is a robot.
        #
        # columns to keep:ip,date,time,cik,extention
        # merge with masters' data by accession and cik
    def process_day(self, date_dir, day_file):
        path_day = self.config.data_path + '/' + date_dir + '/' + day_file
        zf = zipfile.ZipFile(path_day)
        zp_list = zipfile.ZipFile.namelist(zf)
        csv_regex = re.compile('(.*)\.csv')
        df = pd.DataFrame(data={})
        for file in zp_list:
            matcher = csv_regex.match(file)
            if (matcher):
                df = pd.read_csv(zf.open(file), header=0, 
                 usecols=['ip','date','time','cik','accession',
                 'extention','code','size','idx','crawler','browser'],
                 dtype={'ip':object,'date':object,'time':object,'cik':np.float64,'accession':object,
                 'extention':object,'code':np.float64,'size':np.float64,'idx':np.float64,
                 'crawler':np.float64,'browser':object})
                self.logging.debug('Processing day: %s', file)
                self.logging.debug('original size:%s', str(df.size))
                
                df.cik = df.cik.astype(np.int64)
                df = df[(df.crawler == np.float64(0)) & (df.idx == np.float64(0)) & (df.code < self.config.error_code_limit)]
                df = df[['ip', 'date', 'time', 'cik', 'accession', 'extention']]
                self.logging.debug('after removeing crawerls, index, codes: %s', str(df.size))
                
                downloads_count = df.ip.value_counts()
                downloads_count = downloads_count[downloads_count<self.config.threshold].index
                df = df[df.ip.isin(downloads_count)]
                self.logging.debug('after removing robots:%s', str(df.size))
        
        data_merged = pd.merge(df, self.masters, how='left', left_on=['accession', 'cik'], 
                               right_on=['Filename', 'CIK'])
        data_merged = data_merged[['ip', 'date', 'time', 'cik', 'accession', 
                                   'extention', 'Form Type','Date Filed']]
        return data_merged
    
    
    #check if appending the two datasets the size is bigger than output_size_gb
    def check_chunks(self, df1, df2):
        mem_usage_1 = (round(df1.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        mem_usage_2 = (round(df2.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        self.logging.info(str(mem_usage_1 + mem_usage_2) + ' MG')
        chunks = math.trunc((mem_usage_1 + mem_usage_2)/self.config.output_size_mb)
        self.logging.debug('chunks=%s', str(chunks))
        return (chunks > 0)
    
    #get amount of chunks based on output_size_gb
    def get_chunks(self, df):
        mem_usage_1 = (round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        return math.trunc(mem_usage_1/self.config.output_size_mb)
    
    #upload file to dropbox
    #if there is an error when uploading, files would be located in results path
    def save_csv(self, df, year, idx):
        year_idx = year + '_' + str(idx) + '.csv'
        file_from = self.config.results_path + '/' + year_idx
        file_to = self.config.dropbox_folder + year + '/' + year_idx
        df.to_csv(file_from, index=False)
        self.logging.info('Uploading file: %s', file_from)
        upload = True
        try:
           self.transferData.upload_file(file_from, file_to)
        except Exception as err:
           logging.error('Failed to upload %s\n%s', file_from, err)
           upload = False
        if upload:
           os.remove(file_from)
        return idx+1
    
    
    #divide file into chunks and upload to dropbox          
    def save_data(self, df, year, idx):
        chunks = self.get_chunks(df)
        if (chunks==0):
            idx = self.save_csv(df, year, idx)
        else:
            for chunk in np.array_split(df, chunks):
                idx = self.save_csv(chunk, year, idx)
        return idx
        
    
    #load data from master files and clean it
    def load_master(self):
        self.logging.info('Loading masters')
        masters = pd.DataFrame(data={})
        try:
            for master_file in listdir(self.config.master_path):
                self.logging.info('Loading master file:%s', master_file)
                master = pd.read_csv(self.config.master_path + '/' + master_file,
                                     header=None, dtype=object, sep='|')
                master.rename(columns={0:'CIK', 1:'Company Name', 
                                       2:'Form Type', 3:'Date Filed', 
                                       4:'Filename', 5:'Html'}, inplace=True)
                #keep columns of interest
                master = master[['Filename', 'CIK', 'Form Type','Date Filed']]
                #append
                masters = masters.append(master)
                
            #modify filename data to keep accession number
            masters.Filename = masters.Filename.apply(lambda x: x.split('/')[3].replace('.txt', ''))
            #change type of CIK
            masters.CIK = masters.CIK.astype(np.int64)

        except Exception as err:
            logging.error('There has been an error loading master files\n%s', err)
        self.masters = masters
        return masters
    
    #process files for a specific year
    #for each file process day files
    #append to dataframe until the reaches the size
    #save file into dropbox
    def process_year(self, year):
        try:
            df = pd.DataFrame(data={})
            regex_zip = re.compile('log([0-9]{4})([0-9]{2})([0-9]{2}).zip')
            idx = 0
            
            self.logging.info('Processing year:%s', year)
            try:
                self.transferData.create_folder(self.config.dropbox_folder + year)
            except Exception as err:
                logging.warning('Error when creating folder for year:%s\n%s', year, err)
             
            for day_file in listdir(self.config.data_path + '/' + year):
                if regex_zip.match(day_file):
                    try:
                        self.logging.info('Processing day:%s', day_file)
                        df_day = self.process_day(year, day_file)
                        if (self.check_chunks(df,df_day)):
                            idx = self.save_data(df, year, idx)
                            df = df_day
                        else:
                            df = df.append(df_day)
                    
                    except Exception as err:
                        logging.error('There has been an error processing day %s\n%s', day_file, err)
                        
            if (df.shape[0]>0):
                self.logging.info('Saving last chunck for year:%s', year)
                idx = self.save_data(df, year, idx)    
                
            self.logging.info('Finished processing year:%s', year)

        except Exception as err:
            logging.error('There has been an error processing year:%s\n%s', year, err)
               
    #for each year folder, process days files
    def process_data(self):
        try:
            date_dirs = [f for f in listdir(self.config.data_path) if isdir(join(self.config.data_path, f))]
            regex_dir = re.compile('([0-9]{4})')
            for year in date_dirs:
                if (regex_dir.match(year)):
                    self.process_year(year)
                    
        except Exception as err:
            logging.error('There has been an error processing data\n%s', err)
         
