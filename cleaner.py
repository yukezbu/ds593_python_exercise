import sqlite3
import pandas as pd

# Database name
database_file = 'health_events_data.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)

# Load the data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM events", conn)

# 1. Handle missing values

# Fill missing numerical values with the mean of the column
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Fill missing categorical values with the mode of the column
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# 2. Remove duplicate rows
df = df.drop_duplicates()

# 3. Standardize formatting of text columns
# Strip extra spaces, standardize to lowercase, etc.
for col in categorical_columns:
    df[col] = df[col].str.strip().str.lower().str.capitalize()

# 4. Correct obvious data entry errors
# Example: Suppose we want to correct misspellings in the 'City' column
# (Adjust based on actual known errors)
df['City'] = df['City'].replace({
    'newyork': 'New York',
    'la': 'Los Angeles'
    # Add more corrections as needed
})

# 5. Save the cleaned data back into a new table in the SQLite database
df.to_sql('cleaned_data', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Data cleaning completed and saved to 'cleaned_data' table.")
