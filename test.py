#!/bin/python

from transfer import TransferData

#transferData = TransferData("2rC-Zk7vvjAAAAAAAAAAKi13Wv9XgQqtAO0cGdgj2qyCnJyku3LLrzQBzhTd6M-h", 200)
transferData = TransferData("2rC-Zk7vvjAAAAAAAAAALJJBX7liUbhCIPQGngXPVu48P_lOOjJcRvXDxvIX4jUb", 20000)

file_from="/home/mikleal/results/2014_0.csv"
file_to="/EDGAR data 14-17/2014_0.csv"
#file_from="/home/mikleal/edger-cleaner/test.txt"
#file_to="/EDGAR_data_14_17/test.txt"
transferData.upload_file(file_from, file_to)

