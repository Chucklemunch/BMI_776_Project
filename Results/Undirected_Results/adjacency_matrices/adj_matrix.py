import numpy as np
import pandas as pd

genie3 = pd.read_csv('../GENIE3_net_gene_symbols_undirected.tsv', sep='\t')
grnboost2 = pd.read_csv('../GRNBoost2_net_gene_symbols_undirected.tsv', sep='\t')
pidc = pd.read_csv('../PIDC_net_gene_symbols_undirected.tsv', sep='\t')

# get shared genes
genes_genie3 = set(genie3['TF']) | set(genie3['target'])
genes_grnboost2 = set(grnboost2['TF']) | set(grnboost2['target'])
genes_pidc = set(pidc['TF']) | set(pidc['target'])

shared_genes = sorted(genes_genie3 & genes_grnboost2 & genes_pidc)
print(f"Number of shared genes: {len(shared_genes)}")

gene_idx = {gene: i for i, gene in enumerate(shared_genes)}

# build adjacency matrix
def build_adj_matrix(df, shared_genes, gene_idx):
    n = len(shared_genes)
    adj = np.zeros((n, n))
    for _, row in df.iterrows():
        tf, tgt, score = row['TF'], row['target'], row['importance']
        if tf in gene_idx and tgt in gene_idx:
            i, j = gene_idx[tf], gene_idx[tgt]
            adj[i, j] = score
            adj[j, i] = score  # assume undirected
    return adj

adj_genie3 = build_adj_matrix(genie3, shared_genes, gene_idx)
adj_grnboost2 = build_adj_matrix(grnboost2, shared_genes, gene_idx)
adj_pidc = build_adj_matrix(pidc, shared_genes, gene_idx)

pd.DataFrame(adj_genie3, index=shared_genes, columns=shared_genes).to_csv('adjacency_GENIE3.csv')
pd.DataFrame(adj_grnboost2, index=shared_genes, columns=shared_genes).to_csv('adjacency_GRNBoost2.csv')
pd.DataFrame(adj_pidc, index=shared_genes, columns=shared_genes).to_csv('adjacency_PIDC.csv')

