import sqlite3
import pandas as pd

# Database and CSV file names
csv_file = 'funny_epidemiological_events.csv'
database_file = 'health_events_data.db'

# Load CSV into a pandas DataFrame
df = pd.read_csv(csv_file)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create a table with column names based on the CSV headers
# Adjust the table creation SQL based on the actual columns and data types in the CSV file
columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
create_table_query = f'CREATE TABLE IF NOT EXISTS events ({columns})'
cursor.execute(create_table_query)

# Insert data into the table
df.to_sql('events', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Data from {csv_file} has been successfully imported into {database_file}.")
