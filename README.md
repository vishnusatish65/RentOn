CRUD application using file operations on CSV files. 

### Functionalities:

The app allows owner to list their properties with all the details of the property. The users of the can view all the properties listed and rent a house based on availability.

### Read Module :

read_function.py is a function to read a file and return the file data as an object.

```python
import csv
import json

def read(a):
    csv_file = open(f'data\{a}.csv','r')
    csv_reader = csv.DictReader(csv_file)
    return csv_reader
```

### Write Module :

write_function.py is a function to write details to the csv file.

```python
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
```# RentOn