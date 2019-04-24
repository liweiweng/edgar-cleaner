#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import sys
import getopt
from processor import Processor

def info():
    print('clean_edgar.py -p <path> -r <results_path>')

def main(argv):
   path = ''
   master_path = ''
   results = ''
   year = ''
   try:
      opts, args = getopt.getopt(argv,'hp:m:r:y:',['path=','master=','results=', 'year='])
   except getopt.GetoptError:
      info()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-p', '--path'):
         path = arg
      elif opt in ('-m', '--master'):
         master_path = arg
      elif opt in ('-r', '--results'):
         results = arg
      elif opt in ('-y', '--year'):
         year = arg
   if (year==''):
       processor = Processor(path, master_path, results)
       processor.process_data()
   else:
       processor = Processor(path, master_path, results)
       processor.process_year(year)
   
if __name__ == "__main__":
    main(sys.argv[1:])

#python clean_edgar.py -p '/Volumes/TOSHIBA EXT/rawEDGAR/' -m '/Volumes/TOSHIBA EXT/master index files/' -r '/Users/mikaelapisanileal/Documents/SASUniversityEdition/myfolders' -y '2014'