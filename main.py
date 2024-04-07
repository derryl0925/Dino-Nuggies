import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the style for matplotlib plots
plt.style.use('ggplot')

# ----- Cleaning Dinosaur Data -----
# Load the dinosaur data, selecting only the 'cc' column which contains country codes
dino_df = pd.read_csv('dinoData.csv', usecols=['cc'])

# Count the occurrences of each country code and sort by this count in descending order
count_df = dino_df.groupby('cc').size().reset_index(name='count')
count_df = count_df.sort_values(by='count', ascending=False)

# Save the clean data with country occurrences to a CSV file
count_df.to_csv('dinosaur_country_counts.csv', index=False)

# Print the sorted country counts to verify the operation was successful
print(count_df)

# ----- Cleaning Fossil Fuel Data -----
# Attempt to load the fossil fuel data with UTF-8 encoding, falling back to latin1 if necessary
try:
    fuel_df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='utf-8')
except UnicodeDecodeError:
    fuel_df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='latin1')

# List columns that are not required for further analysis
columns_to_remove = [
    "Gas consumption(m³)",
    "Coal consumption(Ton)",
    "Oil consumption(m³)",
    "Gas consumption per capita(m³)",
    "Coal consumption per capita(Ton)",
    "Oil consumption per capita(m³)"
]

# Drop the unnecessary columns from the fossil fuel data
fuel_df = fuel_df.drop(columns_to_remove, axis=1)

# Aggregate the remaining data by 'Entity', which represents countries, excluding the 'World' entry
grouped_df = fuel_df.groupby('Entity').sum()
grouped_df = grouped_df.drop(index='World', errors='ignore')

# Print the aggregated data to verify the operation was successful
print(grouped_df)

# Save the cleaned and aggregated fossil fuel data to a CSV file
grouped_df.to_csv('Fuel_production_vs_consumption_modified.csv', index=False)

# Sort the data by production metrics for different fuel types
sorted_oil_df = grouped_df.sort_values(by='Oil production(m³)', ascending=False)
sorted_gas_df = grouped_df.sort_values(by='Gas production(m³)', ascending=False)
sorted_coal_df = grouped_df.sort_values(by='Coal production(Ton)', ascending=False)

# Print the sorted data for each fuel type to verify the operation was successful
print("Most oil production:")
print(sorted_oil_df)

print("\nMost gas production:")
print(sorted_gas_df)

print("\nMost coal production:")
print(sorted_coal_df)

# Load the CSV file into a DataFrame, addressing the DtypeWarning by setting low_memory=False
hackoil_df = pd.read_csv('hackOil.csv', low_memory=False)

# Check the actual column names in the DataFrame
print(hackoil_df.columns)

# Columns to be removed (update this list if the actual names are different)
columns_to_remove = ["unit", "dataType", "quality", "sourceID", "grade"]

# Make sure the columns you want to remove actually exist in the DataFrame
existing_columns = [col for col in columns_to_remove if col in hackoil_df.columns]

# Remove the specified columns that exist
hackoil_df = hackoil_df.drop(existing_columns, axis=1)

# Links to data sources (for reference only, not executed as code)
# https://paleobiodb.org/classic/displayDownloadGenerator
# https://www.kaggle.com/datasets/shawkatsujon/worldwide-fuel-production-and-consumption
