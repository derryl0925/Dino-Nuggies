import pandas as pd
import plotly.graph_objects as go

# Load your data
dino_counts = pd.read_csv('dinosaur_country_counts.csv')
fossil_fuel_production = pd.read_csv('hackOil_cleaned.csv')

# Convert 'volume' to a numeric type, ensuring non-numeric characters are removed
fossil_fuel_production['volume'] = pd.to_numeric(
    fossil_fuel_production['volume'].str.replace(',', '', regex=True), errors='coerce'
)

# Ensure 'cc' is a string and strip any whitespace
dino_counts['cc'] = dino_counts['cc'].astype(str).str.strip()
fossil_fuel_production['cc'] = fossil_fuel_production['cc'].astype(str).str.strip()

# Aggregate fossil fuel production by country
fossil_fuel_totals = fossil_fuel_production.groupby('cc')['volume'].sum().reset_index()

# Merge the datasets on the country code
merged_data = pd.merge(dino_counts, fossil_fuel_totals, on='cc', how='outer').fillna(0)

# Country centroids for demonstration purposes (usually obtained from a reliable source)
country_centroids = {
    'US': {'lat': 37.0902, 'lon': -95.7129},
    'CA': {'lat': 56.1304, 'lon': -106.3468},
    'ES': {'lat': 40.4637, 'lon': -3.7492},
    'CN': {'lat': 35.8617, 'lon': 104.1954},
    'NZ': {'lat': -40.9006, 'lon': 174.8860},
    # ... additional countries
}

# Initialize the figure
fig = go.Figure()

# Add a choropleth layer for dinosaur findings
fig.add_trace(go.Choropleth(
    locations=dino_counts['cc'],  # Country codes column
    z=dino_counts['count'],  # Data column for color scale
    text=dino_counts['cc'],  # Hover text
    colorscale='Viridis',
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Dinosaur Findings',
))

# Add scatter points for each country's fossil fuel production
for cc, row in merged_data.iterrows():
    if cc in country_centroids:
        fig.add_trace(go.Scattergeo(
            lon=[country_centroids[cc]['lon']],
            lat=[country_centroids[cc]['lat']],
            text=f"{cc}: {row['volume']}",  # Customize this text as needed
            marker=dict(
                size=row['volume'] / 1000,  # Adjust the size as necessary
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
