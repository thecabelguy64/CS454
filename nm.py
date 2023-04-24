# CS454, Assignment 4. Python code written by Cabel McCandless
# In this assignment, we will try to answer this question by analyzing the data 
# to determine how difficult or easy it is to afford a house between any two years.
###################################################################################################################################################
# Part 1 (70 points)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read in the MEHOINUSNMA646N.csv file
mhi_df = pd.read_csv("MEHOINUSNMA646N.csv")

# Read in the NMSTHPI.csv file
hpi_df = pd.read_csv("NMSTHPI.csv")

# Convert the 'DATE' column in both dataframes to datetime objects
mhi_df['DATE'] = pd.to_datetime(mhi_df['DATE'])
hpi_df['DATE'] = pd.to_datetime(hpi_df['DATE'])

# Set the 'DATE' column as the index for both dataframes
mhi_df.set_index('DATE', inplace=True)
hpi_df.set_index('DATE', inplace=True)

# Resample both dataframes to yearly frequency and compute the mean values
mhi_df = mhi_df.resample('Y').mean()
hpi_df = hpi_df.resample('Y').mean()

# Merge the two dataframes and fill in any missing years with NaN values
merged_df = pd.merge(mhi_df, hpi_df, on='DATE', how='outer', sort=True)
    
# Fill in any missing MHI or HPI values with NaN
merged_df['MEHOINUSNMA646N'].fillna(value=np.nan, inplace=True)
merged_df['NMSTHPI'].fillna(value=np.nan, inplace=True)

# Calculate the differences between consecutive MHI values and store in a new column 'D_MHI'
merged_df['D_MHI'] = merged_df['MEHOINUSNMA646N'].diff()

# Calculate the percentage changes between consecutive HPI values and store in a new column 'R_HPI'
merged_df['R_HPI'] = merged_df['NMSTHPI'].pct_change() 

# Rename the index column to 'YEAR'
merged_df.index = pd.to_datetime(merged_df.index).year
merged_df.index.name = 'YEAR'

# Rename the columns to match the specified names
merged_df.columns = ['MHI', 'HPI', 'D_MHI', 'R_HPI']

# Print the merged dataframe
print(merged_df)

# Save the merged dataframe to a CSV file
merged_df.to_csv('nm.csv')

###########################################################################################################################
# Part 2 (30 points)

# Read the nm.csv file with column names
df = pd.read_csv('nm.csv', names=['YEAR', 'MHI', 'HPI', 'D_MHI', 'R_HPI'], skiprows=1)

# Convert YEAR column to integer type
df['YEAR'] = df['YEAR'].astype(int)

# Get the valid years where there is data in both MHI and HPI datasets
valid_years = sorted(list(set(df.dropna()['YEAR'])))

# Define a function to get the missing years
def get_missing_years(years):
    missing_years = []
    for i in range(len(years) - 1):
        if years[i+1] - years[i] > 1:
            missing_years.extend(range(years[i]+1, years[i+1]))
    return missing_years

# Get the missing years
missing_years = get_missing_years(valid_years)

# Combine the missing years with the valid years and sort the list
all_years = sorted(valid_years + missing_years)

# Print the valid years in a user-friendly format
print('Valid years are', end=' ')
i = 0
while i < len(valid_years):
    start_year = valid_years[i]
    end_year = start_year
    
    while i < len(valid_years) - 1 and valid_years[i+1] == end_year + 1:
        end_year = valid_years[i+1]
        i += 1
        
    if start_year == end_year:
        print(start_year, end='')
    elif end_year - start_year == 1:
        print(start_year, ',', end_year, sep='', end='')
    else:
        print( start_year, '-', end_year, ',', sep='', end='')
    
    i += 1

print('\b.', end='')

# Get base year input from user and validate it
print()
while True:
    try:
        base_year = int(input('Enter the base year: '))
        if base_year not in valid_years:
            print('Invalid input. Base year must be a valid year.')
        else:
            break
    except ValueError:
        print('Invalid input. Base year must be an integer.')
        
# Get target year input from user and validate it
while True:
    try:
        target_year = int(input('Enter the target year: '))
        if target_year not in valid_years:
            print('Invalid input. Target year must be a valid year.')
        elif target_year == base_year:
            print('Invalid input. Target year must be different from base year.')
        else:
            break
    except ValueError:
        print('Invalid input. Target year must be an integer.')
        
print('Base year:', base_year)
print('Target year:', target_year)

###########################################################################################################################
# Part 3 (100 points)

# Load data
mhi_df = pd.read_csv("MEHOINUSNMA646N.csv")
hpi_df = pd.read_csv("NMSTHPI.csv")
cpi_df = pd.read_csv("USACPIALLMINMEI.csv")

# Convert date columns to datetime format
mhi_df["DATE"] = pd.to_datetime(mhi_df["DATE"])
hpi_df["DATE"] = pd.to_datetime(hpi_df["DATE"])
cpi_df["DATE"] = pd.to_datetime(cpi_df["DATE"])

# Load the MHI dataset
mhi_df = mhi_df.dropna()  # Remove any rows with missing values
mhi_df["Year"] = pd.to_datetime(mhi_df["DATE"]).dt.year  # Extract the year from the "DATE" column

# Load the HPI dataset
hpi_df = hpi_df.dropna()  # Remove any rows with missing values
hpi_df["Year"] = pd.to_datetime(hpi_df["DATE"]).dt.year  # Extract the year from the "DATE" column

# Load the CPI dataset
cpi_df = cpi_df.dropna()  # Remove any rows with missing values
cpi_df["Year"] = pd.to_datetime(cpi_df["DATE"]).dt.year  # Extract the year from the "DATE" column

# Get average values for base year
mhi_base = mhi_df[mhi_df.Year == base_year].mean()["MEHOINUSNMA646N"]
hpi_base = hpi_df[hpi_df.Year == base_year].mean()["NMSTHPI"]
cpi_base = cpi_df[cpi_df.Year == base_year].mean()["USACPIALLMINMEI"]

# Calculate factors for target year compared to base year
mhi_factor = mhi_df[mhi_df.Year == target_year].mean()["MEHOINUSNMA646N"] / mhi_base
hpi_factor = hpi_df[hpi_df.Year == target_year].mean()["NMSTHPI"] / hpi_base
cpi_factor = cpi_df[cpi_df.Year == target_year].mean()["USACPIALLMINMEI"] / cpi_base

# Calculate factor changes for each data point
mhi_changes = mhi_df.groupby("Year").mean()["MEHOINUSNMA646N"] / mhi_base
hpi_changes = hpi_df.groupby("Year").mean()["NMSTHPI"] / hpi_base
cpi_changes = cpi_df.groupby("Year").mean()["USACPIALLMINMEI"] / cpi_base

# Calculate % difference
percent_change = ((1-(hpi_factor/mhi_factor))*100)
rounded_percent_change = round(percent_change, 2)
abs_percent_change = abs(rounded_percent_change)

# Create plot
fig, ax = plt.subplots(figsize=(12.8, 6.4))
ax.plot(mhi_changes.index, mhi_changes, label="MHI", linestyle=":", color="blue")
ax.plot(hpi_changes.index, hpi_changes, label="HPI", linestyle="-", color="red")
ax.plot(cpi_changes.index, cpi_changes, label="CPI", linestyle="-.", color="olive")

# Add vertical line and horizontal line for base year
ax.axvline(base_year, linestyle='--', color="peru")
ax.axhline(1.0, linestyle='--', color="peru")

# Add vertical line and horizontal line for target year
ax.axvline(target_year, linestyle='--', color="green")
ax.axhline(mhi_factor, linestyle='--', color="green")

# Add textboxes with factors at the target year
mhi_text = r"$\frac{\mathrm{MHI}_{\mathrm{" + str(target_year) + r"}}}{\mathrm{MHI}_{\mathrm{" + str(base_year) + r"}}}$" + f" = {mhi_factor:.2f}"
hpi_text = r"$\frac{\mathrm{HPI}_{\mathrm{" + str(target_year) + r"}}}{\mathrm{HPI}_{\mathrm{" + str(base_year) + r"}}}$" + f" = {hpi_factor:.2f}"
ax.annotate(mhi_text, xy=(target_year, mhi_factor), xytext=(target_year-8, mhi_factor+0.05),
            color="black", bbox=dict(facecolor='yellow', alpha=0.5), arrowprops=dict(arrowstyle="->"))
ax.annotate(hpi_text, xy=(target_year, hpi_factor), xytext=(target_year-8, hpi_factor+0.05),
            color="black", bbox=dict(facecolor='yellow', alpha=0.5), arrowprops=dict(arrowstyle="->"))
plt.text(0.97, 0.05, f" It is {'easier' if mhi_factor < 1 else 'harder'} to afford a house in {target_year} compared to {base_year} by {abs_percent_change} %", fontsize=12, transform=ax.transAxes, ha="right", va="bottom", bbox=dict(facecolor='yellow', alpha=0.5))

# Set axis labels and ticks
ax.set_xlabel("Year")
ax.set_ylabel(f"Factor Changes Compared to Year {base_year}")
plt.xticks(rotation=90)
ticks = list(range(1960, 2022, 2)) + [base_year, target_year]
tick_labels = [str(tick) for tick in ticks]
for i, tick in enumerate(ticks):
    if tick == base_year or tick == target_year:
        tick_labels[i] = str(tick)  # keep the label as a string
ax.set_xticks(ticks)
ax.set_xticklabels(tick_labels)
for label in ax.xaxis.get_ticklabels():
    if int(label.get_text()) == base_year or int(label.get_text()) == target_year:
        label.set_color('red')  # set the color of base_year and target_year to red
    else:
        label.set_color('black')  # set the color of other ticks to black
ax.grid(True)

# Set legend
ax.legend(loc="upper left")

# Set padding and save figure as PDF
plt.tight_layout(pad=0.1)
plt.savefig("nm.pdf")
plt.show()



