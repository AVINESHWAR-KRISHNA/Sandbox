import dask.dataframe as dd
from dask.diagnostics import ProgressBar

SERVER_NAME =''
DATABASE =''
DRIVER = 'SQL+Server'
TABLE_NAME = ''
FILE_PATH = 'Data.csv'

ENGINE = f'mssql+pyodbc://{SERVER_NAME}/{DATABASE}?driver={DRIVER}'

dask_optimizations = {
    'assume_missing': True,  # Assume missing values
    'low_memory': True,  # Optimize memory usage
    'dtype': str,  # Use string type for all columns
}

# Create a Dask DataFrame from the CSV file
df = dd.read_csv(FILE_PATH, sep=',', **dask_optimizations)
df = df.astype(str)

# Remove hyphens from column names
df = df.rename(columns=lambda x: x.replace('-', ''))

# Convert NaN values to None to match SQL Server NULL semantics
df = df.where(df.notnull(), None)

# Write the Dask DataFrame to SQL Server
with ProgressBar():
    df.to_sql(TABLE_NAME, ENGINE, if_exists='append', index=False)
