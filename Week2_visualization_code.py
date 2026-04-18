import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("\nGenerating Visuals")

# create an output folder for all of our visualizations
output_folder = 'EDA_Visuals'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# read the csv files
sold = pd.read_csv('Combined_CRMLSSold_Residential.csv', low_memory=False)
listings = pd.read_csv('Combined_CRMLSListing_Residential.csv', low_memory=False)

# columns to analyze
numeric_fields = [
    'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea',
    'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 
    'DaysOnMarket', 'YearBuilt'
]

for col in numeric_fields:
    # a canvas with 3 plots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3,figsize=(18,5))

    # data containing no empty entries
    data = sold[col].dropna()

    # data without top 1%
    max_value = data.quantile(0.99)
    filtered_data = data[data <= max_value]

    # histogram (filtered to exclude top 1%)
    sns.histplot(filtered_data, bins=50, kde=False, ax=ax1, color='steelblue')
    ax1.set_title(f'{col}\nHistogram (Excluding Top 1%)')
    ax1.set_ylabel('Count')

    # boxplot (filtered to exclude top 1%)
    sns.boxplot(x=filtered_data, ax=ax2, color='lightgreen')
    ax2.set_title(f'{col}\nBoxplot (Excluding Top 1%)')
    

    # boxplot (contains all data)
    sns.boxplot(x=data, ax=ax3, color='salmon')
    ax3.set_title(f'{col}\nBoxplot (Includes All Extremes)')
    
    plt.tight_layout()
    file_path = f"{output_folder}/{col}_distribution.png"
    plt.savefig(file_path)
    plt.close(fig)
    print(f"Saved: {file_path}")
    plt.show()

print(f"\nSuccess! All visuals have been saved to '{output_folder}' folder.")
