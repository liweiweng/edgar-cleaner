#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:29:02 2019

@author: mikaelapisanileal
"""

import edgar
import sys
import getopt

def import_data(local_folder, year_since):
    edgar.download_index(local_folder, year_since)

def info():
    print('python download_edgar.py -d <dir_path> -y <year>')


def main(argv):
    local_folder = ''
    year = 0
    try:
        opts, args = getopt.getopt(argv,'hd:y:',['d=', 'year='])
    except getopt.GetoptError:
        info()
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-d', '--dir'):
         local_folder = arg
      elif opt in ('-y', '--year'):
         year = int(arg)
    
    import_data(local_folder, year)
   
if __name__ == "__main__":
    main(sys.argv[1:])
