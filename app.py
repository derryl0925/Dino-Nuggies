from flask import Flask, jsonify, render_template
import pandas as pd
import plotly.express as px
from plotly.io import to_html

app = Flask(__name__)

# Load the data into Pandas DataFrames
dino_counts = pd.read_csv('dinosaur_country_counts.csv')
fossil_fuel_production = pd.read_csv('hackOil_cleaned.csv')

@app.route('/')
def home():
    # Read the CSV data into Pandas DataFrames
    dino_df = pd.read_csv('dinosaur_country_counts.csv')
    fossil_fuel_df = pd.read_csv('hackOil_cleaned.csv')

   # Example of creating a Plotly figure from the dataframe
    fig_dino = px.bar(dino_df, x='iso3166', y='count', title='Dinosaur Findings by Country')
    fig_fossil_fuel = px.bar(fossil_fuel_df, x='iso3166', y='volume', title='Fossil Fuel Production by Country')

    # Convert the figures to HTML components
    plot_dino_html = to_html(fig_dino, full_html=False)
    plot_fossil_fuel_html = to_html(fig_fossil_fuel, full_html=False)

    # Pass the HTML components to the template
    return render_template('index.html', plot_dino_html=plot_dino_html, plot_fossil_fuel_html=plot_fossil_fuel_html)

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Set the style for matplotlib plots
plt.style.use('ggplot')

# ----- Cleaning Dinosaur Data -----
# Load the dinosaur data, selecting only the 'cc' column which contains country codes
dino_df = pd.read_csv('dinoData.csv', usecols=['cc'])
dino_df = dino_df.rename(columns={'cc': 'iso3166'})

# Count the occurrences of each country code and sort by this count in descending order
count_df = dino_df.groupby('iso3166').size().reset_index(name='count')
count_df = count_df.sort_values(by='count', ascending=False)


# Save the clean data with country occurrences to a CSV file
count_df.to_csv('dinosaur_country_counts.csv', index=False)

# Print the sorted country counts to verify the operation was successful
print(count_df)
'''
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
'''

# Load the CSV file into a DataFrame
hackoil_df = pd.read_csv('hackOil.csv', skipinitialspace=True)
hackoil_df.drop(columns=['Unnamed: 10'], inplace=True)
print(hackoil_df)
# Strip leading and trailing spaces from all string-type data
for col in hackoil_df.columns:
    if hackoil_df[col].dtype == object:  # Check if the column is of string type
        hackoil_df[col] = hackoil_df[col].str.strip()  # Remove leading and trailing spaces
        if col == 'year':
            # Remove commas from the 'year' column
            hackoil_df[col] = hackoil_df[col].str.replace(',', '', regex=False)

# Drop the 'subtype' column if it is empty or not needed
print(hackoil_df)
hackoil_df = hackoil_df.sort_values(by='dataType')
print(hackoil_df)
hackoil_df = hackoil_df[hackoil_df['dataType'] == 'PRODUCTION']
hackoil_df.drop('dataType', axis=1, inplace=True, errors='ignore')
print(hackoil_df)


if 'subtype' in hackoil_df.columns:
    hackoil_df.drop('subtype', axis=1, inplace=True)

# Drop the specified columns
columns_to_drop = ['subtype', 'quality', 'sourceId']
hackoil_df.drop(columns_to_drop, axis=1, inplace=True, errors='ignore')

# Save the cleaned DataFrame back to a CSV file
hackoil_df.to_csv('hackOil_cleaned.csv', index=False)



#fix the line under
hackoil_df_2020 = hackoil_df[hackoil_df['year'] == '2018']
#hackoil_df_2020 = hackoil_df_2020[hackoil_df_2020['dataType'] == 'production']




oil_df_2020 = hackoil_df_2020[hackoil_df_2020['fossilFuelType'] == 'gas']
oil_df_2020['volume'] = pd.to_numeric(oil_df_2020['volume'].str.replace(r'\D', ''), errors='coerce')

unit_column = oil_df_2020['unit']

print(oil_df_2020)
#combine the 2 data frames best on the abreaviation here


oil_df_2020['volume'] = oil_df_2020['volume'].apply(lambda x: int(re.sub(r'\D', '', str(x))))
print(oil_df_2020)

grouped_oil_2020 = oil_df_2020.groupby('iso3166')['volume'].sum().reset_index()
grouped_oil_2020['unit'] = 'million barrel a day'
print(grouped_oil_2020)
sorted_grouped_oil_2020 = grouped_oil_2020.sort_values(by='volume', ascending=False)

#sorted_oil_2020 = grouped_oil_2020.sort_values(by='volume', ascending=True)


# Print the sorted DataFrame
print(sorted_grouped_oil_2020)




# Links to data sources (for reference only, not executed as code)
# https://paleobiodb.org/classic/displayDownloadGenerator
# https://www.kaggle.com/datasets/shawkatsujon/worldwide-fuel-production-and-consumption
