#this file has function to write in csv
import csv
import json
# 'a' refer to the file name, 'b' refers to the data to write, 'c' refer to whether to write a new file or append to the data.
def write(a,b,c):
    if c == "w":
        header = a[0].keys()
        csv_file = open(f'data\{b}.csv',f'{c}',newline = "")
        csv_writer = csv.DictWriter(csv_file,fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(a)
# if we have to append
    else:
        header = a.keys()
        csv_file = open(f'data\{b}.csv',f'{c}',newline = "")
        csv_writer = csv.DictWriter(csv_file,fieldnames=header)
        csv_writer.writerow(a)

    return {"updated"}