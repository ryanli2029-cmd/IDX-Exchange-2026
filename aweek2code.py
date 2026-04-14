import pandas as pd
import numpy as np

sold = pd.read_csv('Combined_CRMLSSold_Residential.csv', low_memory=False)
listings = pd.read_csv('Combined_CRMLSListing_Residential.csv', low_memory=False)

#make sure the listing types are residential
sold = sold[sold['PropertyType'] == 'Residential']
listings = listings[listings['PropertyType'] == 'Residential']

#prints out the unique property types
print("\n Unique Property Types found: ")
print(sold['PropertyType'].unique())

#sold = sold.replace(r'^\s*$', np.nan, regex=True)
sold = sold.replace(['None', 'null', 'NULL', 'NaN'], np.nan)

#a series of the null counts for each column
null_counts = sold.isnull().sum()

#a series containing the null percentages for each column
null_percents = (null_counts / len(sold)) * 100

print("\nNull percents per column")
print(null_percents)

#filter the series to only contain 90% or higher
high_null_percents = null_percents[null_percents > 90]
print("\nColumns with >90% missing values:")
print(high_null_percents)


#numeric distribtion summary
print("\nNumeric Distribution Summary: ")
numeric_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
filtered = sold[numeric_cols]
print(filtered.describe())
