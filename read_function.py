#this reads csv files
import csv
import json

def read(a):
    csv_file = open(f'data\{a}.csv','r')
    csv_reader = csv.DictReader(csv_file)
    return csv_reader