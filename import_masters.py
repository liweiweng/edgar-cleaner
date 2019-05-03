#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:10:53 2019

@author: mikaelapisanileal
"""

#https://github.com/edouardswiac/python-edgar

import edgar
import sys
import getopt
from config import Config


def info():
    print('import_masters.py -p <config_path>')

def main(argv):
   config_path = ''
   try:
      opts, args = getopt.getopt(argv,'hc:',['config_path='])
   except getopt.GetoptError:
      info()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-c', '--config_path'):
         config_path = arg

   config = Config(config_path)
   edgar.download_index(config.master_path, config.since_year)

   
if __name__ == "__main__":
    main(sys.argv[1:])
