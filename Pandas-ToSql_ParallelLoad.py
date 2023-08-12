import os
import datetime
import time
import pandas as pd
from sqlalchemy import create_engine,event
import concurrent.futures
import gc
gc.enable()

startT = time.time()



SERVER_NAME =  ''
DATABASE = ''
DRIVER = 'ODBC Driver 11 for SQL Server'
TABLE_NAME = ''
FTP = 'Test.csv'
CHUNK_SIZE = 10000
MAX_THREADS = 10

insert_records_failure_flag_counter = 0
rows_inserted = 0
insertion_err = ''
insert_records_failure_flag = True

try:

    print(f"Connecting to Server to insert data into table :: {TABLE_NAME}.")
    ENGINE = create_engine(f'mssql+pyodbc://{SERVER_NAME}/{DATABASE}?driver={DRIVER}',fast_executemany=True)

except Exception as e:

    print(f"Unable to connect to server :: {SERVER_NAME} err_msg :: {e}.")


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

def insert_records(chunk):

    try:
        global rows_inserted, insert_records_failure_flag,insertion_err,insert_records_failure_flag_counter

        chunk = chunk.rename(columns=lambda x: x.replace('-', ''))
        chunk.fillna('NULL', inplace=True)

        with ENGINE.connect() as CONN:
            chunk.to_sql(TABLE_NAME, CONN, index=False, if_exists="append", schema="dbo")
            CONN.commit()
        
        CONN.close()
        rows_inserted += len(chunk)

    except Exception as e:

        CONN.rollback()
        insertion_err += str(e)

        insert_records_failure_flag_counter += 1

        print(f"Unable to insert data in table :: {TABLE_NAME}. err_msg :: {insertion_err}")


def create_chunk(df):

    global insertion_err

    chunks = [df[i:i+CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

        @event.listens_for(ENGINE, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

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

    matching_file = FTP

    if matching_file:
        df = pd.read_csv(matching_file,sep=',',low_memory=False)
        create_chunk(df)

    else:
        print("No file found. Sys exit.")