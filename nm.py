# CS454, Assignment 4. Python code wrtitten by Cabel McCandless
# In this assignment, we will try to answer this question by analyzing the data 
# to determine how difficult or easy it is to afford a house between any two years.

# Part 1 (70 points)

import pandas as pd
import numpy as np

# Load the MHI and HPI datasets from their respective CSV files
mhi_df = pd.read_csv('MHI.csv')
hpi_df = pd.read_csv('HPI.csv')

# Merge the MHI and HPI datasets on the 'DATE' column
merged_df = pd.merge(mhi_df, hpi_df, on='DATE', how='outer')

# Convert the 'DATE' column to a datetime object and set it as the index
merged_df['DATE'] = pd.to_datetime(merged_df['DATE'])
merged_df = merged_df.set_index('DATE')

# Resample the DataFrame to an annual frequency, taking the mean for each year
merged_df = merged_df.resample('A').mean()

# Calculate the difference between consecutive elements in the MHI column
merged_df['D_MHI'] = merged_df['MHI'].diff()

# Calculate the percentage change between consecutive elements in the HPI column
merged_df['R_HPI'] = merged_df['HPI'].pct_change() * 100

# Rename the columns to match the specified names
merged_df.columns = ['MHI', 'HPI', 'D_MHI', 'R_HPI']

# Drop rows with NaN values in all columns
merged_df = merged_df.dropna(how='all')

# Create a new index with all years between the first and last year of the DataFrame
year_range = pd.date_range(start=merged_df.index[0], end=merged_df.index[-1], freq='A')
merged_df = merged_df.reindex(year_range)

# Save the DataFrame to a CSV file
merged_df.to_csv('nm.csv')

# Print the resulting DataFrame
print(merged_df)


