# python3 -m pip install numpy 
# python3 -m pip install pandas
# python3 -m pip install sqlalchemy
# python3 -m pip install matplotlib
import matplotlib.pyplot as plt
import psycopg2

con = psycopg2.connect(
    host='__.redshift.amazonaws.com', 
    user='__',
    port=5439,
    password='__',
    dbname='__')
# get connection then get cursor
cur = con.cursor()

# Use the cursor to execute the queries.
all_dat = cur.execute("SELECT * FROM candy_survey;")
# Use the cursor to fetch all of the data
all_dat2 = cur.fetchall()

# use numpy and pandas
import numpy as np 
data = np.any(all_dat==np.nan)
#print(data)

import pandas as pd 
from sqlalchemy import create_engine
data_f = pd.read_sql('Select * from candy_survey;', con)
#print(data_f)

DF_all = pd.DataFrame(all_dat2)
print(DF_all.describe())

print(DF_all.head())
#notice that the column names are not assigned 
# Save the column names
ColName = pd.read_sql("select ordinal_position as position,column_name, column_default as default_value from information_schema.columns where table_name = 'candy_survey' and table_schema = 'public' order by ordinal_position;",con)
ColName = pd.DataFrame(ColName)
print(ColName.column_name)
# Save the column names to specify them in the rename method
renaming = {}
for i in range(71):
	 renaming[i]= ColName.column_name[i]

print(renaming)
# Time to rename them now 
DF_all.rename(columns=renaming, inplace=True)


# Observe the head of the data frame with column names
print(DF_all.head()) 

# Look at unique values for going out and gender  
print(DF_all['goingout'].unique())  
print(DF_all['gender'].unique())


# Lets look at the people who are & aren't going trick or treating
all_go_out = DF_all[DF_all['goingout']=='Yes']
all_not_going_out = DF_all[DF_all['goingout']=='No']
# Find the counts of all columns by gender
c_gend = all_go_out.groupby('gender').count()
c_gend_no = all_not_going_out.groupby('gender').count()
print(c_gend)
print(c_gend_no)

# print only the gender and going out column using the calculations previously made
print(c_gend.goingout)
print(c_gend_no.goingout)

# Create a figure for going out
# Label the x and y axis and add a title
plt.figure()
plt.subplot()
plt.xlabel('Biological Gender')
plt.ylabel('Going Out Count')
plt.title('Trick or Treaters Going out by Gender')
# call bar for a bar plot of gender with the height corresponding to tricker or treaters that are going out
bar_plot = plt.bar(all_go_out['gender'].unique(),c_gend.goingout)

# add labels to add precision in the bar chart
plt.bar_label(bar_plot, padding=2)

# show the plot from the terminal 
plt.show()

# Do another figure for the not going out
plt.figure()
plt.subplot()
plt.xlabel('Biological Gender')
plt.ylabel('Not Going Out Count')
plt.title('Trick or Treaters Not Going out by Gender')
# call bar for a bar plot of gender with the height corresponding to tricker or treaters that are going out
bar_plot2 = plt.bar(all_not_going_out['gender'].unique(),c_gend_no.goingout)
# show the plot from the terminal 

# add labels to add precision in the bar chart
plt.bar_label(bar_plot2, padding=2)
plt.show()

# Close any cursors and connections made 
cur.close()
con.close()
