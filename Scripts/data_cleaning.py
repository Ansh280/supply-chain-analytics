import pandas as pd

df = pd.read_csv('../data/DataCoSupplyChainDataset.csv', encoding='latin-1')

# Drop fully/mostly empty columns
df = df.drop(columns=['Product Description', 'Order Zipcode'])

# Drop irrelevant PII columns
df = df.drop(columns=[
    'Customer Email', 'Customer Password', 'Customer Fname',
    'Customer Lname', 'Customer Street', 'Customer Zipcode',
    'Product Image'
])

# Convert date columns to proper datetime
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])

# Confirm shape after cleaning
print("Cleaned shape:", df.shape)
print("Remaining columns:", df.columns.tolist())

# Save cleaned version
df.to_csv('../data/cleaned_supply_chain.csv', index=False)
print("Saved cleaned_supply_chain.csv")