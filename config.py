#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:47:47 2019

@author: mikaelapisanileal
"""

from properties.p import Property


class Config:
    def __init__(self, path):
        prop = Property()
        config = prop.load_property_files(path)
        self.log_level = config['log_level']
        self.access_token = config['access_token']
        self.threshold= int(config['threshold'])
        self.error_code_limit=int(config['error_code_limit'])
        self.output_size_mb=int(config['output_size_mb'])
        self.dropbox_folder=config['dropbox_folder']
        self.dropbox_chunck=int(config['dropbox_chunck'])
        self.dropbox_timeout=float(config['dropbox_timeout'])
        self.data_path=config['data_path']
        self.master_path=config['master_path']
        self.results_path=config['results_path']
        self.since_year=int(config['since_year'])
        
