#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:47:47 2019

@author: mikaelapisanileal
"""

from properties.p import Property
from transfer import TransferData

class Config:
    def __init__(self, path):
        prop = Property()
        self.config = prop.load_property_files(path)
        self.transferData = TransferData(self.config['access_token'])
        self.threshold= int(self.config['threshold'])
        self.error_code_limit=int(self.config['error_code_limit'])
        self.output_size_mb=int(self.config['output_size_mb'])
        self.access_token=self.config['access_token']
        self.dropbox_folder=self.config['dropbox_folder']
        self.rows_master_skip=self.config['rows_master_skip']
        self.data_path=self.config['data_path']
        self.master_path=self.config['master_path']
        self.results_path=self.config['results_path']
        
        def get_transferData(self):
            return self.transferData
        
        def get_threshold(self):
            return self.threshold
        
        def get_error_code_limit(self):
            return self.error_code_limit
        
        def get_output_size_mb(self):
            return self.output_size_mb
        
        def get_access_token(self):
            return self.access_token
        
        def get_dropbox_folder(self):
            return self.dropbox_folder
        
        def get_rows_master_skip(self):
            return self.rows_master_skip
        
        def get_data_path(self):
            return self.data_path
        
        def get_master_path(self):
            return self.master_path
        
        def get_results_path(self):
            return self.results_path

