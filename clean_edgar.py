#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import sys
import getopt
from processor import Processor
from config import Config

def info():
    print('clean_edgar.py -p <path> -r <results_path>')

def main(argv):
   config_path = ''
   year = ''
   try:
      opts, args = getopt.getopt(argv,'hc:y:',['config=', 'year='])
   except getopt.GetoptError:
      info()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-c', '--config'):
         config_path = arg
      elif opt in ('-y', '--year'):
         year = arg
   config = Config(config_path)
   processor = Processor(config)
   if (year==''):
       processor.process_data()
   else:
       processor.process_year(year)
   
if __name__ == "__main__":
    main(sys.argv[1:])

#python clean_edgar.py -c 'config.properties' -y '2014'