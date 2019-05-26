import pandas as pd
import numpy as np

df = pd.read_csv('data-0-4_tab_header_cleaned.csv', header=[0], sep='\t') 
print('All columns names:')
print(list(df.columns))

print('Print all datas')
print(df)


print('Seleect only some datas:')
print(df.loc[(df['Couleur'] >= 11) & (df['Altitude'] >= 2000)])