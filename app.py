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

count_df['iso3166'] = count_df['iso3166'].str.strip()

count_df['iso3166'] = count_df['iso3166'].str.lower()
#print(count_df)



# Load the CSV file into a DataFrame

hackoil_df = pd.read_csv('hackOil.csv', skipinitialspace=True)

hackoil_df.drop(columns=['Unnamed: 10'], inplace=True)
#print(hackoil_df)
#hackoil_df.drop(columns=['Unnamed: 10'], inplace=True)

# Strip leading and trailing spaces from all string-type data
for col in hackoil_df.columns:
    if hackoil_df[col].dtype == object:  # Check if the column is of string type
        hackoil_df[col] = hackoil_df[col].str.strip()  # Remove leading and trailing spaces
        if col == 'year':
            # Remove commas from the 'year' column
            hackoil_df[col] = hackoil_df[col].str.replace(',', '', regex=False)

# Drop the 'subtype' column if it is empty or not needed

#hackoil_df = hackoil_df.sort_values(by='dataType')

hackoil_df = hackoil_df[hackoil_df['dataType'] == 'PRODUCTION']
#print(hackoil_df)

hackoil_df.drop('dataType', axis=1, inplace=True, errors='ignore')




if 'subtype' in hackoil_df.columns:
    hackoil_df.drop('subtype', axis=1, inplace=True)

# Drop the specified columns
columns_to_drop = ['subtype', 'quality', 'sourceId']
hackoil_df.drop(columns_to_drop, axis=1, inplace=True, errors='ignore')

# Save the cleaned DataFrame back to a CSV file

#print(hackoil_df)




hackoil_df_2020 = hackoil_df[hackoil_df['year'] == '2020']
#print(hackoil_df_2020)


oil_df_2020 = hackoil_df_2020[hackoil_df_2020['fossilFuelType'] == 'oil']
print(oil_df_2020)
oil_df_2020['volume'] = oil_df_2020['volume'].str.replace(',', '')
oil_df_2020['volume'] = oil_df_2020['volume'].str.replace(r'[,()]', '', regex=True)
oil_df_2020['volume'] = pd.to_numeric(oil_df_2020['volume'])

unit_column = oil_df_2020['unit']

#print(oil_df_2020)
#combine the 2 data frames best on the abreaviation here


#oil_df_2020['volume'] = oil_df_2020['volume'].apply(lambda x: int(re.sub(r'\D', '', str(x))))
#print(oil_df_2020)

grouped_oil_2020 = oil_df_2020.groupby('iso3166')['volume'].sum().reset_index()
grouped_oil_2020['unit'] = 'million barrel a day'
#print(grouped_oil_2020)

sorted_grouped_oil_2020 = grouped_oil_2020.sort_values(by='volume', ascending=False)

#sorted_oil_2020 = grouped_oil_2020.sort_values(by='volume', ascending=True)


# Print the sorted DataFrame
#print(sorted_grouped_oil_2020)

country_counts = count_df.groupby('iso3166')['count'].sum().reset_index()

#print(country_counts)



merged_df = pd.merge(count_df, sorted_grouped_oil_2020, on='iso3166', how='inner')

merged_df.to_csv('merged_data.csv', index=False)
#print(merged_df)
merged_df.rename(columns={'iso3166': 'country'}, inplace=True)
print(merged_df)
merged_df.to_csv('merged_data.csv', index=False)
#print(sorted_grouped_oil_2020)


#print("Missing countries:", missing_countries)





# Links to data sources (for reference only, not executed as code)
# https://paleobiodb.org/classic/displayDownloadGenerator
