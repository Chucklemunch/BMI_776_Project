import pandas as pd
import requests
import sys
import time
import pickle


args = sys.argv
algo = None

found_interactions = {}

file_paths = {
    'GENIE3' : '../Results/Undirected_Results/GENIE3_net_gene_symbols_undirected.tsv',
    'GRNBoost2' : '../Results/Undirected_Results/GRNBoost2_net_gene_symbols_undirected.tsv',
    'PIDC' : '../Results/Undirected_Results/PIDC_net_gene_symbols_undirected.tsv'
}

# Make sure args are correct 
if len(args) == 1:
    print(f'Checking predicted interaction for all algos')

    found_interactions = {
        'GENIE3' : [],
        'GRNBoost2' : [],
        'PIDC' : []
    }
    
elif len(args) == 2:
    algo = args[1]
    print(f'Checking predicted interaction for {algo}')
    file_paths = {algo : file_paths[algo]}

    found_interactions = {
        algo : []
    }
    
elif len(args) >= 2 or args[1] not in ['GENIE3', 'GRNBoost2', 'PIDC']:
    print('BioGRID_Test.py usage: \n\n python BioGRID_Test.py <GENIE3/GRNBoost2/PIDC> \n\n')
    exit(1)

for algo, file_path in file_paths.items():
    print(f'Checking predicted interaction for {algo}')
    
    df = pd.read_csv(file_path, sep="\t")
    
    # sort by importance + keep top 100
    # top_df = df.sort_values(by="importance", ascending=False).head(100)

    # sort by importance + keep top 100
    top_df = df.sort_values(by="importance", ascending=False).head(500)
    
    # BioGRID API setup 
    BIOGRID_ACCESS_KEY = "a207ffa23db79e55a7d7a5a69b79f0c9"
    BIOGRID_URL = "https://webservice.thebiogrid.org/interactions/"
    
    def query_biogrid(gene1, gene2):
        params = {
            "accesskey": BIOGRID_ACCESS_KEY,
            "format": "json",
            "geneList": f"{gene1}|{gene2}",
            "searchNames": "true",
            "includeInteractors": "false",
            "includeHeader": "true"
        }
        try:
            response = requests.get(BIOGRID_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return len(data) > 0  # true if interaction found
        except requests.exceptions.Timeout:
            print(f"Timeout when querying {gene1}, {gene2}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error when querying {gene1}, {gene2}: {e}")
        except Exception as e:
            print(f"Unexpected error for {gene1}, {gene2}: {e}")
        return False
    
    
    # loop through top pairs + check BioGRID
    verified_count = 0
    for index, row in top_df.iterrows():
        gene1, gene2 = row['TF'], row['target']
        found = query_biogrid(gene1, gene2)
        if found:
            print('Found: ', gene1, gene2)

            # Add to results dictionary
            found_interactions[algo].append((gene1, gene2))
            verified_count += 1
        time.sleep(1)  # API rate limits
    
    print(f"{verified_count}/100 interactions found in BioGRID")

print(found_interactions)

# Output results
with open('../Results/found_interactions_dict_500.pickle', 'wb') as f:
    pickle.dump(found_interactions, f)
