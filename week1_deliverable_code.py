import pandas as pd
import glob

# grab all the 2024 csv files from the folder
sold_files = glob.glob('CRMLSSold2024*.csv') + glob.glob('CRMLSSold2025*.csv')
listing_files = glob.glob('CRMLSListing2024*.csv') + glob.glob('CRMLSListing2025*.csv')

sold_list = []
listing_list = []

# load sold files and print row counts for the deliverable
print("Sold files: ")
for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    print(file, "has", len(df), "rows")
    sold_list.append(df)

# load listing files and print row counts
print("\nListing files: ")
for file in listing_files:
    df = pd.read_csv(file, low_memory=False)
    print(file, "has", len(df), "rows")
    listing_list.append(df)

# put all the individual months together into one big dataframe
sold_combined = pd.concat(sold_list, ignore_index=True)
listings_combined = pd.concat(listing_list, ignore_index=True)

print("\nTotal combined sold rows:", len(sold_combined))
print("Total combined listing rows:", len(listings_combined))

# filter the datasets to only keep Residential properties
sold_filtered = sold_combined[sold_combined['PropertyType'] == 'Residential']
listings_filtered = listings_combined[listings_combined['PropertyType'] == 'Residential']

#confirm row counts
print("\nResidential sold rows:", len(sold_filtered))
print("Residential listing rows:", len(listings_filtered))

# save the cleaned datasets as new CSV files
sold_filtered.to_csv('Combined_CRMLSSold_Residential.csv', index=False)
listings_filtered.to_csv('Combined_CRMLSListing_Residential.csv', index=False)

