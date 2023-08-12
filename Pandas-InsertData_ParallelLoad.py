import os
import sys
import datetime
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text, bindparam
import concurrent.futures
import gc
gc.enable()

startT = time.time()

SERVER_NAME = ''
DATABASE = ''
DRIVER = ''
TABLE_NAME = ''
FTP = ''
MAX_THREADS = ''
CHUNK_SIZE = ''
FILENAME = ''
LOGFILE = ''

insert_records_failure_flag_counter = 0
rows_inserted = 0
insertion_err = ''
insert_records_failure_flag = True

try:

    print(f"Connecting to Server to insert data into table :: {TABLE_NAME}.")
    ENGINE = create_engine(f'mssql+pyodbc://{SERVER_NAME}/{DATABASE}?driver={DRIVER}',fast_executemany=True)

except Exception as e:

    print(f"Unable to connect to server :: {SERVER_NAME} err_msg :: {e}.")

    print("Sys exit.")
    sys.exit(1)

def get_matching_file(FTP):

    try:
        print(f"Looking for file in path :: {FTP}")

        current_date = datetime.datetime.now().strftime('%Y%m%d')

        for file_name in os.listdir(FTP):
            if file_name.endswith(current_date+'.csv'):
                print(f"File found :: {file_name}")
                return os.path.join(FTP, file_name)
        
        print(f"No matching file found for system current date :: {current_date} in folder :: {FTP}.")
        return None
    
    except Exception as e:
        print(f"Error occured while looking for file in folder :: {FTP}. err_msg :: {e}")

        print("Sys exit.")
        sys.exit(1)

def insert_records(chunk):

    try:
        global rows_inserted, insert_records_failure_flag,insertion_err,insert_records_failure_flag_counter

        cnx = ENGINE.connect()

        chunk = chunk.rename(columns=lambda x: x.replace('-', ''))
        chunk.fillna('NULL', inplace=True)

        float_columns = chunk.select_dtypes(include='float').columns
        chunk[float_columns] = chunk[float_columns].replace([np.inf, -np.inf], np.nan)
        chunk[float_columns] = chunk[float_columns].astype(pd.Int64Dtype())

        insert_query = f"INSERT INTO {TABLE_NAME} ({', '.join(chunk.columns)}) VALUES ({', '.join([':' + col for col in chunk.columns])})"

        with cnx.begin() as transaction:
            stmt = text(insert_query)
            stmt = stmt.bindparams(*[bindparam(col) for col in chunk.columns])
            cnx.execute(stmt, chunk.to_dict(orient='records'))
            transaction.commit()
        
        cnx.close()
        rows_inserted += len(chunk)

    except Exception as e:

        insertion_err += str(e)

        insert_records_failure_flag_counter += 1

        print(f"Unable to insert data in table :: {TABLE_NAME}. err_msg :: {insertion_err}")


def create_chunk(df):

    global insertion_err

    chunks = [df[i:i+CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

        futures = []

        print(f"Inserting data into table :: {TABLE_NAME}.")

        for chunk in chunks:
            future = executor.submit(insert_records,chunk)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future)
    
    print(f"Data inserted successfully into table :: {TABLE_NAME}.")
    print(f"Total number of rows inserted :: {rows_inserted}.")
    print("Process completed successfully.")

    Success_percentage = (rows_inserted/len(df)) * 100
    Success_Per = "Success Percentage :: {:.2f}%".format(Success_percentage)

    print(Success_Per)

    endT = time.time()
    TotalT = endT - startT
    hours, remainder = divmod(TotalT, 3600)
    minutes, seconds = divmod(remainder, 60)

    Script_Time = "Total time taken :: {:.0f} hr {:.0f} min {:f} sec".format(hours, minutes, seconds)

    print(Script_Time)


if __name__ == '__main__':

    matching_file = get_matching_file(FTP)

    if matching_file:
        df = pd.read_csv(matching_file,sep=',')
        create_chunk(df)

    else:

        print("No file found. Sys exit.")
        sys.exit(1) 