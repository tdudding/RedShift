'''
import the data into an s3 bucket after creating one from the console. 
--> later create one from script
Have to have access point from the internet open to public (note if sensitive data use a different route.)
'''
import boto3
s3 = boto3.resource('s3',
	aws_access_key_id = 'AKIA5VXSMAGSU4NNLDUU',
	aws_secret_access_key = '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')
bucket = s3.Bucket('candybucket00000001')
s3.Object('candybucket00000001', 'candy_fix.csv').put(Body=open('/Users/tdudding/Desktop/DataWarehouse/candy_fixed1.csv', 'rb'))







