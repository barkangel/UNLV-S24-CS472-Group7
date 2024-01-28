import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Read data from CSV file
df = pd.read_csv('data/Brandon_newoutput.csv')

# Shorten file directory names
df['Shortened_Filename'] = df['Filename'].apply(lambda x: os.path.basename(x))

# Extract year from the 'Date' column
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Define color map for committers
committers = df['Committer'].unique()
committer_colors = {committer: plt.cm.get_cmap('tab10')(i) for i, committer in enumerate(committers)}

# Increase figure size for better visibility
plt.figure(figsize=(12, 8))

# Plot scatter plot with distinct colors for each committer
for committer, color in committer_colors.items():
    subset_df = df[df['Committer'] == committer]
    plt.scatter(subset_df['Shortened_Filename'], subset_df['Year'], label=committer, c=color, s=100, alpha=0.8, edgecolors='w')

# Add labels and title
plt.xlabel('Filename')
plt.ylabel('Year')
plt.title('Scatter Plot of Filename vs Year (Colored by Committer)')

# Add legend
plt.legend(title='Committers')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')  # 'ha' parameter aligns x-axis labels to the right

# Automatically adjust subplot parameters for better layout
plt.tight_layout()

plt.show()
