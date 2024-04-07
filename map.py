import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Error Handling and Certificate Verification

from geopy.geocoders import Nominatim
from certifi import where


# Load the data from CSV files
dino_data = pd.read_csv("dinosaur_country_counts.csv")
oil_data = pd.read_csv("hackOil.csv")

# Filter for oil data (considering only data for UAE for simplicity)
oil_data_filtered = oil_data[oil_data["iso3166"] == "ae"]

# Get the latitude and longitude data from the ISO codes (using geopy)
geolocator = Nominatim(user_agent="my-script", ssl_context=ssl.create_default_context(cafile=where()))

def get_lat_lon(iso_code):
  location = geolocator.geocode(iso_code)
  if location:
    return location.latitude, location.longitude
  else:
    print(f"Warning: Could not geocode ISO code: {iso_code}")
    return None, None  # Handle missing locations gracefully

# Get latitude and longitude for dino data
dino_data["latitude"], dino_data["longitude"] = zip(
    *dino_data["iso3166"].apply(get_lat_lon)
)

# Get latitude and longitude for oil data (assuming single country)
oil_latitude, oil_longitude = get_lat_lon("ae")

# Create a Basemap projection
worldmap = Basemap(projection="millers", llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180)

# Convert dinosaur data latitude and longitude to map projection coordinates
dino_x, dino_y = worldmap(dino_data["longitude"], dino_data["latitude"])

# Plot the dinosaur markers (adjust marker size and color as desired)
worldmap.scatter(dino_x, dino_y, s=50, c="red", alpha=0.7, label="Dinosaur Fossils")

# Plot the oil production marker (assuming single country)
oil_x, oil_y = worldmap.convert(oil_longitude, oil_latitude)
worldmap.plot(oil_x, oil_y, marker="o", markersize=20, color="blue", label="Oil Production")

# Draw coastlines and political boundaries
worldmap.drawcoastlines()
worldmap.drawcountries()

# Fill continents (optional)
worldmap.fillcontinents(color='lightgray')

# Add a title and legend
plt.title("Dinosaur Fossils and Oil Production (Sample Data)")
plt.legend()

# Display the map
plt.show()
