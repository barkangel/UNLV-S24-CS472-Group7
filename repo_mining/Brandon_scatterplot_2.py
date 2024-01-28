import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Read data from CSV file
df = pd.read_csv('data/Brandon_newoutput.csv') 

# Shorten file directory names
df['Shortened_Filename'] = df['Filename'].apply(lambda x: os.path.basename(x))

# Extract week and year from the 'Date' column
df['Week'] = pd.to_datetime(df['Date']).dt.isocalendar().week
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Define color map for years
years = df['Year'].unique()
year_colors = {year: plt.cm.get_cmap('tab10')(i) for i, year in enumerate(years)}

# Increase figure size for better visibility
plt.figure(figsize=(15, 10))

# Plot scatter plot with distinct colors for each year
for year, color in year_colors.items():
    subset_df = df[df['Year'] == year]
    plt.scatter(subset_df['Shortened_Filename'], subset_df['Week'], label=str(year), c=color, s=100, alpha=0.8, edgecolors='w')

# Add labels and title
plt.xlabel('Filename')
plt.ylabel('Week')
plt.title('Scatter Plot of Filename vs Week (Colored by Year)')

# Add legend
plt.legend(title='Year')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Automatically adjust subplot parameters for better layout
plt.tight_layout()

plt.show()
