#-------------------------------------------------------
                    # Imports & File

# the csv library = iterate over the data
# the ast library = determine data type

# longest list = longest values in character length for varchar column 
# headers lsit = column names
# type_list    = updating column types as we iterate over our data


# pip3 install psycopg2-binary 

import csv, ast, psycopg2

#file_directory = input("Input the file's directory with anything that needs to be put in the path befor: ")
#file_name = input("Input the file name with the extension: ")
#to_open = file_directory+'/'+file_name

f = open("/Users/__/Desktop/__/candy_fixed1.csv", 'r')
reader = csv.reader(f)

longest, headers, type_list = [], [], []
# -------------------------------------------------------

'''
Need to evaluate every value and cast to the most restrictive option,
 from decimalized numbers to integers, and from integers to strings.

First the data_type function determines if the value is text or a number, 
    then for the appropriate type of number if needed. 
It will consume both the new data, 
    and the current best type to evaluate against.
'''
import sys
import os
def dataType(val, current_type):
            # Evaluates numbers to an appropriate type, and strings an error
    try:
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar (25)'
    except SyntaxError:
        return 'varchar (25)'
    if type(t) in [int, float]:
        if (type(t) in [int]) and current_type not in ['float', 'varchar']:
            # Use smallest possible int type
            if (1 < t < 32767) and current_type not in ['int', 'bigint']:
                return 'smallint'
            elif (1 < t < 2147483647) and current_type not in ['bigint']:
                return 'int'
            else:
                return 'bigint'
        if type(t) is float and current_type not in ['varchar']:
            return 'decimal'
    else:
        return 'varchar (25)'


# --------------------------------------------------------------------------------
 # Iterate over the rows in the CSV, call our function data_type, and populate the lists 
    # longest, header, and type_list.

for row in reader:
    if len(headers) == 0:
        headers = row
        for col in row:
            longest.append(0)
            type_list.append('')
    else:
        for i in range(len(row)):
                        # NA is the csv null value
            if type_list[i] == 'varchar' or row[i] == 'NA':
                pass
            else:
                var_type = dataType(row[i], type_list[i])
                type_list[i] = var_type
        if len(row[i]) > longest[i]:
            longest[i] = len(row[i])
f.close()

# ----------------------------------------------------------------------------------
'''
    Write SQL statement based on what the lists are
'''

statement = 'create table candy_survey ('

for i in range(len(headers)):
    if type_list[i] == 'varchar':
        statement = (statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
    else:
        statement = (statement + '\n' + '{} {}' + ',').format(headers[i].lower(), type_list[i])

statement = statement[:-1] + ');'
print(statement)


# ------------------------------------------------------------------------------------
'''
  	Use the data from the S3 buckets and connect to the redshift cluster created in the aws console 
'''
conn = psycopg2.connect(
    host='__.redshift.amazonaws.com', 
    user='__',
    port=5439,
    password='__',
    dbname='__')

# to get my connection correct I had to edit the security group to allow inbound for my IP (or all IP)

cur = conn.cursor()

cur.execute(statement)
# this will be the strucuture of the table with columns and col_values
conn.commit()

# this will actually take the data and put it in the table
# must not use the access point must use the object directly from main bucket
sql = """copy candy_survey from 's3://candysurveybucket/candy_fix.csv'
    access_key_id '___'
    secret_access_key '___'
    region '__'
    ignoreheader 1
    null as 'NA'
    removequotes
    delimiter ',';"""
cur.execute(sql)
conn.commit()

cur.close()
conn.close()
