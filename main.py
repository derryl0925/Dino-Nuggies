import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')


# Cleaning Dinosaur data
# Load the CSV file into a DataFrame
df = pd.read_csv('DinoNuggieFindings.csv')

# Columns to be removed
columns_to_remove = ["occurrence_no", "record_type", "reid_no", "collection_no", "accepted_attr", "accepted_no", "max_ma", "min_ma", "reference_no", "time_bins", "time_contain", "time_major", "time_buffer", "time_overlap"]

# Remove the specified columns
df = df.drop(columns_to_remove, axis=1)

# Save the modified DataFrame back to a CSV file
df.to_csv('DinoNuggieFindings_modified.csv', index=False)

# Cleaning fossil fuel data
# Load the CSV file into a DataFrame
#df = pd.read_csv('Fuel_production_vs_Consumption.csv')
try:
    df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='latin1')


# Columns to be removed
columns_to_remove = [
    "Gas consumption(m³)", 
    "Coal consumption(Ton)", 
    "Oil consumption(m³)", 
    "Gas consumption per capita(m³)", 
    "Coal consumption per capita(Ton)", 
    "Oil consumption per capita(m³)"
]

# Remove the specified columns
df = df.drop(columns_to_remove, axis=1)

grouped_df = df.groupby('Entity').sum()
grouped_df = grouped_df.drop(index='World', errors='ignore')

print(grouped_df)

# Save the modified DataFrame back to a CSV file
df.to_csv('Fuel_production_vs_consumption_modified.csv', index=False)

sorted_oil_df = grouped_df.sort_values(by='Oil production(m³)', ascending=False)

# Sort by most gas production
sorted_gas_df = grouped_df.sort_values(by='Gas production(m³)', ascending=False)

# Sort by most coal production
sorted_coal_df = grouped_df.sort_values(by='Coal production(Ton)', ascending=False)

print("Most oil production:")
print(sorted_oil_df)

print("\nMost gas production:")
print(sorted_gas_df)

print("\nMost coal production:")
print(sorted_coal_df)





'''
https://paleobiodb.org/classic/displayDownloadGenerator
https://www.kaggle.com/datasets/shawkatsujon/worldwide-fuel-production-and-consumption
'''