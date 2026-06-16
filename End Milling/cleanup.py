import pandas as pd

file_path = 'stlml_10.txt'

df = pd.read_csv(file_path, sep='\t', skiprows=21)

df.columns = df.columns.str.strip()

df.to_csv('run10.csv', index=False)

print("Conversion complete: run2.csv")