import pandas as pd

gene_expression_matrix = pd.read_csv('gene_expression_matrix.tsv', sep='\t')
column_headers = gene_expression_matrix.columns.tolist()

gene_expression_filtered = pd.read_csv('gene_expression_filtered.tsv', sep='\t', header=None)

# check that dimensions match
if len(column_headers) != gene_expression_filtered.shape[0]:
    raise ValueError("Number of column headers does not match number of rows in gene_expression_filtered.tsv")

gene_expression_filtered.insert(0, "Gene", column_headers)
gene_expression_filtered_T = gene_expression_filtered.T

# save without index
gene_expression_filtered_T.to_csv('gene_expr_filtered_w_headers_T.tsv', sep='\t', index=False, header=False)

