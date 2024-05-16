#!usr/bin/env python=3

import os
import pandas as pd
from itertools import combinations
import multiprocessing
import time

# Set the number of cores you requested
n_procs = int(os.environ.get("NSLOTS"))

def parse_hpoa_file(file_path):
    # Specify the columns you want to keep
    columns_to_keep = ["database_id", "disease_name", "hpo_id"]

    # Read the HPOA file into a Pandas DataFrame with selected columns
    hpo_df = pd.read_csv(file_path, sep='\t', comment='#', header=0, usecols=columns_to_keep)

    return hpo_df

# Example usage
file_path = "phenotype (3).hpoa"
hpo_data = parse_hpoa_file(file_path)

# Finding the number of unique diseases in this dataset
unique_diseases = hpo_data['disease_name'].unique()
total_unique_diseases = len(unique_diseases)
print("\nTotal Unique diseases:", total_unique_diseases)

#Finding the number of unique phenotypes
unique_phenotypes = hpo_data['hpo_id'].unique()
total_unique_phenotypes = len(unique_phenotypes)
print("\nTotal Unique Phenotypes:", total_unique_phenotypes)

grouped = hpo_data.groupby(['database_id', 'disease_name'])['hpo_id'].apply(list).reset_index()

# # Create an empty list to store common phenotypes information
common_phenotypes_data = []

# Get unique disease names
unique_diseases = grouped['disease_name'].unique()
combos = combinations(unique_diseases, 2)

common_phenotypes_loop=[]
def loop_function(disease_combination):
    disease_1, disease_2 = disease_combination
    
    hpo_list_1 = grouped[grouped['disease_name'] == disease_1]['hpo_id'].iloc[0]
    hpo_list_2 = grouped[grouped['disease_name'] == disease_2]['hpo_id'].iloc[0]
    
    common_phenotypes = [phenotype for phenotype in hpo_list_1 if phenotype in hpo_list_2]
    
    num_phenotypes_1 = len(hpo_list_1)
    num_phenotypes_2 = len(hpo_list_2)
    num_common_phenotypes = len(common_phenotypes)
    
    common_phenotypes_loop.append({
        'Disease 1': disease_1,
        'Disease 2': disease_2,
        'Disease 1 Phenotypes': num_phenotypes_1,
        'Disease 2 Phenotypes': num_phenotypes_2,
        'Common Phenotypes': common_phenotypes,
        'Number of Common Phenotypes': num_common_phenotypes
    })
    
    return common_phenotypes_loop

if __name__=='__main__':
    start = time.time()
    with multiprocessing.Pool(4) as p:
        mp_output = p.map(loop_function, combos)
    end = time.time()
    print("Time: ", end-start)

common_phenotypes_data = [x for xs in mp_output for x in xs]      
df = pd.DataFrame(common_phenotypes_data)
