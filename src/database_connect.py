import argparse

from src.utils import convert_dtypes, data, database, dbconnect, table

parser = argparse.ArgumentParser(
    description = 'Database script toconnect to mysql server, create database, table and insert data to the table.'
    )
parser.add_argument('-cd', '--create_db', type = bool, help = 'Do you wanna create new database or work on existing database ?')
parser.add_argument('-db', '--database_name',type = str, required = True, help = 'Provide a name for the database.')
parser.add_argument('-tb', '--table_name', type = str, help = 'Provide a name for the Table.')
parser.add_argument('-fp', '--file_path', type = str, help = 'Provide filepath.')

args = parser.parse_args()


#Connection to database
db,cr = dbconnect('localhost','root')

args={
    'database_name':'INVENTORY',
    'table_name':'customers',
    'file_path':'data/sales.csv'
}

#Create Database 
if args.create_db:
    databases = database(cr=cr,dbname=args['database_name'])
else:
    #Creating table  
    table(cr=cr,dbname=args['database_name'],tbname=args['table_name'])

    #Insert Values in table Customers
    file_df = data(filepath=args['file_path'])
    types, placeholders = convert_dtypes(file_df)
    
    total = 0
    for _, row in file_df.iterrows():
        sql = f"INSERT INTO {args['table_name']} VALUES ({placeholders})"
        # val = tuple(row)
        # print(val)
        cr.execute(sql, tuple(row))
        db.commit() 
        if cr.rowcount == 1:
            total += 1