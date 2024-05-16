#!/usr/bin/env python3
import os
import pandas as pd
import multiprocessing
from scipy.stats import hypergeom

# Load the DataFrame from output.csv

output_file = "output.csv"
output_df = pd.read_csv(output_file)
total_unique_phenotypes = 10813

# Set the number of cores you requested

n_procs = int(os.environ.get("NSLOTS"))

# Define a function to calculate p-value using hypergeometric test

def calculate_p_value(row):
    # Extract the row data from the tuple
    index, data = row
    
    # Access the elements of the row data using integer indices
    K = data['Number of Common Phenotypes']  # Total number of common phenotypes
    n1 = data['Disease 1 Phenotypes']  # Number of phenotypes for Disease 1
    n2 = data['Disease 2 Phenotypes']  # Number of phenotypes for Disease 2 
    
    # Define parameters for hypergeometric distribution
    N = total_unique_phenotypes  # Total number of unique phenotypes
    
    # Perform hypergeometric test
    p_value = hypergeom.sf(K - 1, N, n1, n2)
    
    return p_value

if __name__ == '__main__':

    with multiprocessing.Pool(n_procs) as p:

        # Calculate p-values using multiprocessing

        p_values = p.map(calculate_p_value, output_df.iterrows()) 

    # Add the p-values to the DataFrame

    output_df['P-Value'] = p_values

# Save the DataFrame with p-values to a new CSV file

output_with_p_values_file = "output_with_p_values.csv"

output_df.to_csv(output_with_p_values_file, index=False)

print("Output with p-values saved to:", output_with_p_values_file)


