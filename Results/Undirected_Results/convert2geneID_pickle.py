import pandas as pd
import pickle

# Load Ensembl ID to gene symbol dictionary
with open('../../Data/SARS-CoV-2/ensembl_gene_dict.pickle', 'rb') as f:
    ensembl_gene_dict = pickle.load(f)

# Step 1: Set values to None if key == value
for key in list(ensembl_gene_dict.keys()):
    if ensembl_gene_dict[key] == key:
        ensembl_gene_dict[key] = None

# Load network files
#df1 = pd.read_csv('GENIE3_network.csv', sep='\t')
df2 = pd.read_csv('../../GRNBoost2/GRNBoost2_network.csv', sep='\t')
df3 = pd.read_csv('../../PIDC/PIDC_inferred_network.txt', sep='\t', header=None)
df3.columns = ['TF', 'target', 'importance']

df1 = pd.read_pickle('../GENIE3/SARS-CoV-2/interactions_dataframe.pickle')
df1.to_csv(sep='\t', header=None)
df1.columns = ['TF', 'target', 'importance']


# Function to convert and filter
def convert_and_filter(df):
    df['TF_symbol'] = df['TF'].map(ensembl_gene_dict)
    df['target_symbol'] = df['target'].map(ensembl_gene_dict)
    df_clean = df.dropna(subset=['TF_symbol', 'target_symbol'])
    df_output = df_clean[['TF_symbol', 'target_symbol', 'importance']]
    df_output.columns = ['TF', 'target', 'importance']
    return df_output

# Process and convert each network
df1_output = convert_and_filter(df1)
df2_output = convert_and_filter(df2)
df3_output = convert_and_filter(df3)

# Save the outputs
df1_output.to_csv('GENIE3_net_gene_symbols.tsv', sep='\t', index=False)
df2_output.to_csv('GRNBoost2_net_gene_symbols.tsv', sep='\t', index=False)
df3_output.to_csv('PIDC_net_gene_symbols.tsv', sep='\t', index=False)

