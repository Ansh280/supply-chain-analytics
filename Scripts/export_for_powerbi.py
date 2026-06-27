import sqlite3
import pandas as pd

conn = sqlite3.connect('../data/supply_chain.db')
df = pd.read_sql_query("SELECT * FROM orders", conn)
df.to_csv('../dashboard/supply_chain_for_powerbi.csv', index=False)
print("Exported:", df.shape)
conn.close()