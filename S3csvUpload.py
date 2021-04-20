'''
import the data into an s3 bucket after creating one from the console. 
Have to have access point from the internet open to public (note if sensitive data use a different route.)
'''
# python3 -m pip install boto3

import boto3
s3 = boto3.resource('s3',
	aws_access_key_id = '__',
	aws_secret_access_key = '__')
bucket = s3.Bucket('candysurveybucket')
s3.Object('candysurveybucket', 'candy_fix.csv').put(Body=open('/Users/__/Desktop/__/candy_fixed1.csv', 'rb'))







