import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the dinosaur data
dino_df = pd.read_csv('dinosaur_country_counts.csv')

# Load the fossil fuel data
fuel_df = pd.read_csv('Fuel_production_vs_consumption_modified.csv')

# Sample data for demonstration
# Assume your dataframes are already structured correctly

# Dinosaur data
dino_data = pd.read_csv('dinosaur_country_counts.csv')

# Fuel production data
try:
    fuel_df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='utf-8')
except UnicodeDecodeError:
    fuel_df = pd.read_csv('Fuel_production_vs_Consumption.csv', encoding='latin1')


fuel_df['Entity'] = fuel_df['Entity'].str.strip()  # Remove leading/trailing whitespaces
dino_df['cc'] = dino_df['cc'].str.strip()          # Remove leading/trailing whitespaces

# Aggregate fossil fuel production by country
fuel_production_by_country = fuel_df.groupby('Entity').sum().reset_index()

# Aggregate dinosaur findings by country
dino_findings_by_country = dino_df.groupby('cc').size().reset_index(name='dino_count')

# Merge the datasets on country
merged_data = pd.merge(fuel_production_by_country, dino_findings_by_country,
                       how='outer', left_on='Entity', right_on='cc').fillna(0)

# Plot the data on a world map
fig = px.choropleth(merged_data, 
                    locations='Entity',
                    locationmode='country names',
                    color='dino_count',
                    hover_name='Entity',
                    hover_data={'dino_count': True, 'Gas production(m³)': True,
                                'Coal production(Ton)': True, 'Oil production(m³)': True},
                    color_continuous_scale='blues',
                    labels={'dino_count': 'Dinosaur Findings', 
                            'Gas production(m³)': 'Gas Production', 
                            'Coal production(Ton)': 'Coal Production', 
                            'Oil production(m³)': 'Oil Production'},
                    title='Dinosaur Findings vs Fossil Fuel Production by Country')

fig.update_geos(showcountries=True)

# Show the map
fig.show()