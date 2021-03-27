#-------------------------------------------------------
					# Imports & File

# the csv library = iterate over the data
# the ast library = determine data type

# longest list = longest values in character length for varchar column 
# headers lsit = column names
# type_list    = updating column types as we iterate over our data

import csv, ast, psycopg2

file_directory = readline("Input the file's directory with anything that needs to be put in the path befor: ")
file_name = readline("Input the file name with the extension: ")
to_open = file_directory+'/'+file_name

f = open(to_open, 'r')
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

def dataType(val, current_type):
	        # Evaluates numbers to an appropriate type, and strings an error
	try:
		t = ast.literal_eval(val)
	except ValueError:
		return 'varchar'
	except SyntaxError:
		return 'varchar'
	if type(t) in [int, long, float]:
		if (type(t) in [int, long]) and current_type not in ['float', 'varchar']:
			# Use smallest possible int type
			if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
				return 'smallint'
			elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
				return 'int'
			else:
				return 'bigint'
		if type(t) is float and current_type not in ['varchar']:
			return 'decimal'
	else:
		return 'varchar'

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

statement = 'create table stack_overflow_survey ('

for i in range(len(headers)):
    if type_list[i] == 'varchar':
        statement = (statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
    else:
        statement = (statement + '\n' + '{} {}' + ',').format(headers[i].lower(), type_list[i])

statement = statement[:-1] + ');'


# --------------------------------------------------------------------------------------------








