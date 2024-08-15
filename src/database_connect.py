import argparse

from src.utils import convert_dtypes, data, database, dbconnect, table, aws_auth, upload_to_s3, download_from_s3

parser = argparse.ArgumentParser(
    description = 'Database script toconnect to mysql server, create database, table and insert data to the table.'
    )
parser.add_argument('-cd', '--create_db', type = bool, help = 'Do you wanna create new database or work on existing database ?')
parser.add_argument('-db', '--database_name',type = str, required = True, help = 'Provide a name for the database.')
parser.add_argument('-tb', '--table_name', type = str, help = 'Provide a name for the Table.')
parser.add_argument('-fp', '--file_path', type = str, help = 'Provide filepath.')
parser.add_argument('-ak', '--Aws_access_keys',type = str, required = True, help = 'Provide a name for the database.')

args = parser.parse_args()


#Connection to database
db,cr = dbconnect('localhost','root')

# args={
#     'database_name':'INVENTORY',
#     'table_name':'customers',
#     'file_path':'data/sales.csv'
# }

#Create Database 
if args.create_db:
    databases = database(cr=cr,dbname=args.database_name)
else:
    #Insert Values in table Customers
    file_df = data(filepath=args.file_path)
    types, placeholders = convert_dtypes(file_df)
    
    #Creating table  
    table(cr=cr,dbname=args.database_name,tbname=args.table_name,col_name= types)

    
    total = 0
    for _, row in file_df.iterrows():
        sql = f"INSERT INTO {args.table_name} VALUES ({placeholders})"
        # val = tuple(row)
        # print(val)
        cr.execute(sql, tuple(row))
        db.commit() 
        if cr.rowcount == 1:
            total += 1
       
#Connection to the AWS S3     
s3 = aws_auth('ap-south-1')

# Upload file to the bucket.
upload_to_s3(s3,'data/test.csv','dtop-project','test.csv')

# Download file from the bucket
download_from_s3(s3,'dtop-project',)