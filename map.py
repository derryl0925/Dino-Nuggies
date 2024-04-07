import pandas as pd
import plotly.graph_objects as go

# Load your data
dino_counts = pd.read_csv('dinosaur_country_counts.csv').rename(columns={'cc': 'iso3166'})
fossil_fuel_production = pd.read_csv('hackOil_cleaned.csv')

# Convert 'volume' to a numeric type, ensuring non-numeric characters are removed
fossil_fuel_production['volume'] = pd.to_numeric(
    fossil_fuel_production['volume'].str.replace(',', '', regex=True), errors='coerce'
)

# Ensure 'iso3166' is a string and strip any whitespace
dino_counts['iso3166'] = dino_counts['iso3166'].astype(str).str.strip()
fossil_fuel_production['iso3166'] = fossil_fuel_production['iso3166'].astype(str).str.strip()

# Aggregate fossil fuel production by country
fossil_fuel_totals = fossil_fuel_production.groupby('iso3166')['volume'].sum().reset_index()

# Merge the datasets on the country code
merged_data = pd.merge(dino_counts, fossil_fuel_totals, on='iso3166', how='outer').fillna(0)

# Define country centroids for plotting
country_centroids = {
    # ... include all necessary country centroids
}

# Initialize the figure
fig = go.Figure()

# Add a choropleth layer for dinosaur findings
fig.add_trace(go.Choropleth(
    locations=merged_data['iso3166'],  # Use merged data iso3166
    z=merged_data['count'],  # Dinosaur counts
    colorscale='Viridis',
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Dinosaur Findings',
))

# Iterate over merged_data instead of just iso3166
for _, row in merged_data.iterrows():
    # Use the iso3166 value from the current row
    iso3166 = row['iso3166']
    if iso3166 in country_centroids:
        fig.add_trace(go.Scattergeo(
            lon=[country_centroids[iso3166]['lon']],
            lat=[country_centroids[iso3166]['lat']],
            text=f"{iso3166}: {row['volume']}",
            marker=dict(
                size=row['volume'] / 1000,  # Adjust the size
                color='red',
                symbol='x'
            ),
        ))

# Update layout for better visibility
fig.update_layout(
    title_text='Dinosaur Findings and Fossil Fuel Production by Country',
    geo=dict(
        showland=True,
        showcountries=True,
        landcolor='rgb(217, 217, 217)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

# Show the figure
fig.show()
