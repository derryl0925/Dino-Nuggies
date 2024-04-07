import pandas as pd
import matplotlib.pyplot as plt

# Set the style for matplotlib plots
plt.style.use('ggplot')

# Load the CSV files into pandas DataFrames
hackoil_df = pd.read_csv('hackOil_cleaned.csv')

# Clean the 'volume' column (remove commas and non-numeric characters)
hackoil_df['volume'] = hackoil_df['volume'].astype(str)  # Ensure it's a string
hackoil_df['volume'] = hackoil_df['volume'].str.replace(r'[^\d]', '', regex=True)  # Remove non-numeric characters
hackoil_df['volume'] = pd.to_numeric(hackoil_df['volume'], errors='coerce')  # Convert to numeric

# Load dinosaur counts data
dino_counts = pd.read_csv('dinosaur_country_counts.csv')

# Continue with your data processing...
# Group hackoil_df by 'fossilFuelType' and 'iso3166', sum the volumes
hackoil_grouped = hackoil_df.groupby(['fossilFuelType', 'iso3166'])['volume'].sum().reset_index()

# Merge the two DataFrames on the country codes ('iso3166' and 'cc')
combined_data = pd.merge(hackoil_grouped, dino_counts, left_on='iso3166', right_on='cc')

# Plotting the graphs
# Set the style for matplotlib plots
plt.style.use('ggplot')

# Define fossil fuel types to plot
fuel_types = combined_data['fossilFuelType'].unique()

for fuel_type in fuel_types:
    # Filter data for each fuel type
    filtered_data = combined_data[combined_data['fossilFuelType'] == fuel_type]

    # Create a scatter plot for each fuel type vs dinosaur occurrences
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data['count'], filtered_data['volume'])
    plt.title(f'Dinosaur Occurrences vs {fuel_type.capitalize()} Production')
    plt.xlabel('Number of Dinosaur Occurrences')
    plt.ylabel(f'{fuel_type.capitalize()} Production Volume')
    plt.tight_layout()
    plt.show()
