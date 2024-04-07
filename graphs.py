import matplotlib.pyplot as plt
import seaborn as sns
import pandas as panda

merged_data = panda.read_csv('merged_data.csv')

#volume sort
sorted_merged_data = merged_data.sort_values(by='volume', ascending=False)
top_20_oil_producers = sorted_merged_data.head(30)

#dino sort
sorted_merged_data = merged_data.sort_values(by='count', ascending=False)
top_20_dino_countries = sorted_merged_data.head(30)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_20_dino_countries, x='country', y='count', palette='viridis')
plt.title('Dinosaur Count by Country (Top 30 Dinosaur Fossil Discoveries)')
plt.xlabel('Top 30 Oil Producing Countries')
plt.ylabel('Dinosaur Fossil Count')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(data=top_20_oil_producers, x='country', y='count', palette='viridis')
plt.title('Dinosaur Count by Country (Top 30 Oil Producers)')
plt.xlabel('Top 30 Oil Producing Countries')
plt.ylabel('Dinosaur Fossil Count')
plt.xticks(rotation=90)
plt.show()

# Plot oil production by country for the top 20 oil-producing countries
plt.figure(figsize=(12, 6))
sns.barplot(data=top_20_oil_producers, x='country', y='volume', palette='magma')
plt.title('Oil Production by Country (Top 30 Oil Producers)')
plt.xlabel('Top 30 Oil Producing Countries')
plt.ylabel('Oil Production (million barrel a day)')
plt.xticks(rotation=90)
plt.show()

# Examine correlation between dinosaur count and oil production for the top 20 oil-producing countries
plt.figure(figsize=(8, 8))
sns.regplot(data=merged_data, x='count', y='volume')
plt.title('Correlation between Dinosaur Count and Oil Production')
plt.xlabel('Dinosaur Fossil Count')
plt.ylabel('Oil Production (million barrel a day)')
plt.show()

correlation_coefficient = merged_data['count'].corr(merged_data['volume'])
print("Pearson correlation coefficient:", correlation_coefficient)