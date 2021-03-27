# RedShift

1. Run the S3 file to upload your candy1.csv file (found in the files here as well)
2. Run the Redshift Finalize Table file.
    * This will create the schema, column names, column types, and upload the data from the S3 bucket to the Redshift Database.
3. Run the Redshift Query file to query your table. 

Things to make these files better:
  -> Use the script to create the S3 bucket
  -> Use the script to create the Redshift cluster
  
Things to note:
  -> The security group within the VPC needs to be configured to allow for inbound requests.
  -> Have an access point for the S3 bucket to allow for an upload.
  -> do NOT use the access point for S3 bucket file upload to Redshift (in SQL copy statement).
  -> must use the S3 bucket main with the file to upload to Redshift (in SQL copy statement).
