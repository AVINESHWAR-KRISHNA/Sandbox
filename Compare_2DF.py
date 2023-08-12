from sqlalchemy import create_engine
import pandas as pd 
import datacompy

try:
    _ServerName = ''
    _Database = ''
    # driver = 'ODBC Driver 17 for SQL Server'
    driver = 'SQL+Server'
    
    ENGINE = create_engine(f'mssql+pyodbc://{_ServerName}/{_Database}?driver={driver}',fast_executemany=True)
    CONN = ENGINE.connect()

except Exception as err:
    print(err)


DF1 = pd.read_sql("select * from tmp", CONN)
DF2 = pd.read_sql("select * from tmp", CONN)

diff = datacompy.Compare(DF1, DF2, join_columns='')
output = diff.report(sample_count=100, column_count=100)

file = open("Mismatch.txt", "w")

for line in output:
    file.writelines(line)

file.close()