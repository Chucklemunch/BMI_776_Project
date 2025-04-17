using NetworkInference
using CSV
using DataFrames

input_file = "gene_expr_filtered_w_headers_T.tsv"
output_file = "PIDC_inferred_network.txt"

# Load data (no transposition)
df = CSV.read(input_file, DataFrame, header=1) 

# Write data to a temporary file (because infer_network expects a file?)
tmp_file = tempname() * ".tsv"
CSV.write(tmp_file, df, delim='\t')

# run PIDC
inferred_network = infer_network(tmp_file, PIDCNetworkInference())
write_network_file(output_file, inferred_network)

# clean up temp file
rm(tmp_file)

