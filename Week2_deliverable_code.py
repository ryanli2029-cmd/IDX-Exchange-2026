import pandas as pd
import numpy as np

sold = pd.read_csv('Combined_CRMLSSold.csv', low_memory=False)
listings = pd.read_csv('Combined_CRMLSListing.csv', low_memory=False)

#prints out the unique property types
print("\n Unique Property Types found: ")
print(sold['PropertyType'].unique())

#make sure the listing types are residential
sold = sold[sold['PropertyType'] == 'Residential']
listings = listings[listings['PropertyType'] == 'Residential']

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

#part 2 of deliverable
print("\nPart 2 of deliverable (enrichment)")

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly=(mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index())

sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')

#merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

print("\nNull mortgage rates in Sold dataset:", sold_with_rates['rate_30yr_fixed'].isnull().sum())
print("\nNull mortgage rates in Listings dataset:", listings_with_rates['rate_30yr_fixed'].isnull().sum())
sold_with_rates.to_csv('Combined_CRMLSSold_Residential_Enriched.csv', index=False)
listings_with_rates.to_csv('Combined_CRMLSListing_Residential_Enriched.csv', index=False)
print("\nSold and Listings Enriched CSV Files Saved Successfully")

print("\nSold Dataset Preview")
# Previewing the sold data using CloseDate
print(
    sold_with_rates[
        ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
    ].head()
)

print("\nListings Dataset Preview")
# Previewing the listings data using ListingContractDate
print(
    listings_with_rates[
        ['ListingContractDate', 'year_month', 'ListPrice', 'rate_30yr_fixed']
    ].head()
)
