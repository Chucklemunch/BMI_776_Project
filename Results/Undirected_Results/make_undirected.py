import pandas as pd

def deduplicate_undirected(df):
    # Remove self-interactions
    df = df[df['TF'] != df['target']].copy()

    # Create a normalized (undirected) interaction key by sorting TF-target pairs
    df['pair'] = df.apply(lambda row: tuple(sorted([row['TF'], row['target']])), axis=1)

    # Keep only the row with the highest importance for each pair
    df = df.sort_values('importance', ascending=False).drop_duplicates(subset='pair', keep='first')

    # Split the pair back into two columns
    df[['TF', 'target']] = pd.DataFrame(df['pair'].tolist(), index=df.index)
    
    return df[['TF', 'target', 'importance']]

# Load each network
df_genie3 = pd.read_csv('GENIE3_net_gene_symbols.tsv', sep='\t')
df_grnboost2 = pd.read_csv('GRNBoost2_net_gene_symbols.tsv', sep='\t')
df_pidc = pd.read_csv('PIDC_net_gene_symbols.tsv', sep='\t')

# Deduplicate
df_genie3_dedup = deduplicate_undirected(df_genie3)
df_grnboost2_dedup = deduplicate_undirected(df_grnboost2)
df_pidc_dedup = deduplicate_undirected(df_pidc)

# Save
df_genie3_dedup.to_csv('GENIE3_net_gene_symbols_undirected.tsv', sep='\t', index=False)
df_grnboost2_dedup.to_csv('GRNBoost2_net_gene_symbols_undirected.tsv', sep='\t', index=False)
df_pidc_dedup.to_csv('PIDC_net_gene_symbols_undirected.tsv', sep='\t', index=False)

