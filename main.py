import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')


# Cleaning Dinosaur data
# Load the CSV file into a DataFrame
df = pd.read_csv('DinoNuggieFindings.csv')

# Columns to be removed
columns_to_remove = ["occurrence_no", "record_type", "reid_no", "collection_no", "accepted_attr", "accepted_no", "max_ma", "min_ma", "reference_no", "time_bins", "time_contain", "time_major", "time_buffer", "time_overlap"]

# Rename the 'accepted_name' column to 'name'
df = df.rename(columns={'accepted_name': 'name'})

# Remove the specified columns
df = df.drop(columns_to_remove, axis=1)

# Save the modified DataFrame back to a CSV file
df.to_csv('DinoNuggieFindings_modified.csv', index=False)

df = pd.read_csv('DinoNuggieFindings_modified.csv')

# Combine 'cc' and 'state' into a new 'location' column
df['location'] = df['cc'] + ', ' + df['state']

# Dino findings by location
location_distribution = df['location'].value_counts()
print(location_distribution)

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

# Save the modified DataFrame back to a CSV file
df.to_csv('Fuel_production_vs_consumption_modified.csv', index=False)


'''
https://paleobiodb.org/classic/displayDownloadGenerator
https://www.kaggle.com/datasets/shawkatsujon/worldwide-fuel-production-and-consumption
'''