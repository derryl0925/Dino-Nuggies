import pandas as pd
import plotly.express as px

# Load the dinosaur data
dino_df = pd.read_csv('DinoNuggieFindings_modified.csv')

# Load the cleaned fossil fuel data
hackoil_df = pd.read_csv('hackOil_cleaned.csv')

# Strip leading/trailing whitespaces from country codes if necessary
hackoil_df['iso3166'] = hackoil_df['iso3166'].str.strip()  # Adjust column name if different
dino_df['cc'] = dino_df['cc'].str.strip()

# Aggregate fossil fuel production by country
# Ensure you're summing up the correct column for total production, 
# adjust 'volume' to the correct column name for total production in your data
fuel_production_by_country = hackoil_df.groupby('iso3166')['volume'].sum().reset_index()

# Aggregate dinosaur findings by country
dino_findings_by_country = dino_df.groupby('cc').size().reset_index(name='dino_count')

# Merge the datasets on the country code
merged_data = pd.merge(fuel_production_by_country, dino_findings_by_country,
                       how='outer', left_on='iso3166', right_on='cc').fillna(0)

# Plot the data on a world map with adjusted color scale and layout
fig = px.choropleth(
    merged_data, 
    locations='iso3166',
    color='dino_count',
    hover_name='iso3166',
    hover_data={'dino_count': True, 'volume': True},
    color_continuous_scale=px.colors.sequential.Plasma,  # More distinct color scale
    range_color=[0, merged_data['dino_count'].max()],  # Set the range of the color scale
    title='Dinosaur Findings vs Fossil Fuel Production by Country'
)

# Update map layout for better visibility
fig.update_geos(
    showcountries=True,
    showcoastlines=True,
    showland=True,
    landcolor='LightGrey'
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title='Dinosaur Findings',
        tickvals=[0, merged_data['dino_count'].max() / 2, merged_data['dino_count'].max()],
        ticktext=['Low', 'Medium', 'High']
    )
)

# Show the map
fig.show()

