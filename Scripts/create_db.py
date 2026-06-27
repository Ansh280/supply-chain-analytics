import sqlite3
import pandas as pd

# Load cleaned data
df = pd.read_csv('../data/cleaned_supply_chain.csv')

# Create SQLite database
conn = sqlite3.connect('../data/supply_chain.db')

# Write dataframe to a table
df.to_sql('orders', conn, if_exists='replace', index=False)

# Confirm it worked
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM orders")
row_count = cursor.fetchone()[0]
print("Rows loaded into database:", row_count)

cursor.execute("PRAGMA table_info(orders)")
columns = cursor.fetchall()
print("\nTable columns:")
for col in columns:
    print(col[1], "-", col[2])

conn.close()
print("\nDatabase created: supply_chain.db")