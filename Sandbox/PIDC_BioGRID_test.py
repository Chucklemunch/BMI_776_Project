import pandas as pd
import requests
import time

df = pd.read_csv("../Results/Undirected_Results/PIDC_net_gene_symbols_undirected.tsv", sep="\t")

# sort by importance + keep top 100
top_df = df.sort_values(by="importance", ascending=False).head(100)

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
        verified_count += 1
    time.sleep(1)  # API rate limits

print(f"{verified_count}/100 interactions found in BioGRID")
