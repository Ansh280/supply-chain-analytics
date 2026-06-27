import pandas as pd

df = pd.read_csv('../data/DataCoSupplyChainDataset.csv', encoding='latin-1')

print("Shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nNull counts per column:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nFirst 5 rows:")
print(df.head())