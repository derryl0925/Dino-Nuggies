import babypandas as bpd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')


# Load the CSV file into a DataFrame
df = pd.read_csv('DinoNuggieFindings.csv')

# Cleaning Dinosaur data, columns to be removed
columns_to_remove = ["occurrence_no", "record_type", "reid_no", "collection_no", "accepted_attr", "accepted_no", "max_ma", "min_ma", "reference_no", "time_bins", "time_contain", "time_major", "time_buffer", "time_overlap"]

# Remove the specified columns
df = df.drop(columns_to_remove, axis=1)

# Save the modified DataFrame back to a CSV file
df.to_csv('DinoNuggieFindings_modified.csv', index=False)
