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
        self.rows_master_skip=int(self.config['rows_master_skip'])
        self.data_path=self.config['data_path']
        self.master_path=self.config['master_path']
        self.results_path=self.config['results_path']
        
