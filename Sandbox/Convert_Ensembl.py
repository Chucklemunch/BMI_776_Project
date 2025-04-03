import pickle
import pandas as pd
import sys
import requests
import json

server = "https://rest.ensembl.org"

gene1_names = []
gene2_names = []
interactions = None

with open('../Results/GENIE3/SARS-CoV-2/interactions_dataframe.pickle', 'rb') as f:
    interactions = pickle.load(f)

with open('../Results/GENIE3/SARS-CoV-2/ranked_interaction_list_500.txt', 'r') as f:
    # Get gene names for Ensembl names
    for interaction in f:
        gene1, gene2, score = interaction.split()

        for i, gene in enumerate([gene1, gene2]):
            ext = f'/xrefs/id/{gene}?'
    
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
             
            if not r.ok:
              r.raise_for_status()
              sys.exit()
             
            decoded = r.json()
            
            gene_name = decoded[-1]['display_id']

            if i == 0:
                gene1_names.append(gene_name)
            else:
                gene2_names.append(gene_name)

interactions['gene1_name'] = pd.Series(gene1_names)
interactions['gene2_name'] = pd.Series(gene2_names)

with open('../Sandbox/genie_interactions_df_with_names.pickle', 'wb') as f:
    pickle.dump(interactions, f)
