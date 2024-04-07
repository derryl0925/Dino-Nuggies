import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry


plt.style.use('ggplot')

country_abbr = {country.name: country.alpha_2 for country in pycountry.countries}

# Cleaning Dinosaur data
# Load the CSV file into a DataFrame
#df = pd.read_csv('dinoData.csv')
df = pd.read_csv('dinoData.csv', usecols=['cc'])


# Save the modified DataFrame back to a CSV file
df.to_csv('dinoDataClean.csv', index=False)
count_df = df.groupby('cc').size().reset_index(name='count')
count_df = count_df.sort_values(by='count', ascending=False)


print(count_df)

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
grouped_df.reset_index(inplace=True)

# Define a dictionary mapping country names to their abbreviations
grouped_df['Entity'] = grouped_df['Entity'].map(country_abbr)

# Replace the country names in grouped_df with their abbreviations
#grouped_df['Entity'] = grouped_df['Entity'].map(country_abbr)
# Alternatively, you can use the replace function
# grouped_df['Entity'].replace(country_abbr, inplace=True)

print(grouped_df)


print(grouped_df)

# Save the modified DataFrame back to a CSV file
df.to_csv('Fuel_production_vs_consumption_modified.csv', index=False)

sorted_oil_df = grouped_df.sort_values(by='Oil production(m³)', ascending=False)

# Sort by most gas production
sorted_gas_df = grouped_df.sort_values(by='Gas production(m³)', ascending=False)

# Sort by most coal production
sorted_coal_df = grouped_df.sort_values(by='Coal production(Ton)', ascending=False)

print("Most oil production:")
#print(sorted_oil_df)

print("\nMost gas production:")
#print(sorted_gas_df)

print("\nMost coal production:")
#print(sorted_coal_df)


#merged_df_oil = pd.merge(count_df, sorted_oil_df, left_on='cc', right_index=True, how='inner')
#merged_df_oil.drop('Entity', axis=1, inplace=True)
#merged_df_oil.to_csv('merged_data_oil.csv', index=False)
#print(merged_df_oil)






'''
https://paleobiodb.org/classic/displayDownloadGenerator
https://www.kaggle.com/datasets/shawkatsujon/worldwide-fuel-production-and-consumption
'''