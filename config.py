#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:47:47 2019

@author: mikaelapisanileal
"""

from properties.p import Property

class Level:
    

class Config:
    def __init__(self, path):
        prop = Property()
        config = prop.load_property_files(path)
        self.log_level = config['log_level']
        self.access_token = config['access_token']
        self.threshold= int(config['threshold'])
        self.error_code_limit=int(config['error_code_limit'])
        self.output_size_mb=int(config['output_size_mb'])
        self.access_token=config['access_token']
        self.dropbox_folder=config['dropbox_folder']
        self.dropbox_chunk=int(config['dropbox_chunk'])
        self.dropbox_timeout=float(config['dropbox_timeout'])
        self.rows_master_skip=int(config['rows_master_skip'])
        self.data_path=self.config['data_path']
        self.master_path=self.config['master_path']
        self.results_path=self.config['results_path']
        self.since_year=int(self.config['since_year'])
        
