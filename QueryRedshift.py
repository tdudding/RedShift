import psycopg2

con = psycopg2.connect(
    host='redshift-cluster-1.ctryexfglqji.us-east-1.redshift.amazonaws.com', 
    user='awsuser',
    port=5439,
    password='This0is1AWS!',
    dbname='dev')

# get connection then get cursor
cur = con.cursor()

# Use the cursor to execute the queries.
all_dat = cur.execute("SELECT * FROM candy_survey;")
# Use the cursor to fetch all of the data
all_dat2 = cur.fetchall()

# use numpy and pandas
import numpy as np 
data = np.any(all_dat==np.nan)
print(data)

import pandas as pd 
from sqlalchemy import create_engine
data_f = pd.read_sql('Select * from candy_survey;', con)
print(data_f)

cur.close()
con.close()
