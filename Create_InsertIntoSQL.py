import pandas as pd

# Read the CSV file using Pandas

df = pd.read_csv('data.csv')

# Initialize an empty string to store the SQL script
sql_script = ''

# Extract the column names and values for each row
for index, row in df.iterrows():
    columns = ', '.join(df.columns)
    values = ''
    for value in row:
        if isinstance(value, str):
            values += f"'{value}', "
        else:
            values += f"{value}, "
    values = values[:-2]

    # Generate the SQL script for the row and append it to the main SQL script
    sql_script += f"INSERT INTO table_name ({columns}) VALUES ({values});\n"

# Write the SQL script to a file
with open('output_script.sql', 'w') as f:
    f.write(sql_script)