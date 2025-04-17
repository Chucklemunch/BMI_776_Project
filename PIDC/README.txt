Install Julia
$ wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.3-linux-x86_64.tar.gz
$ mv julia-1.9.3/ ~/.julia
$ echo 'export PATH=$HOME/.julia/bin:$PATH' >> ~/.bashrc
$ source ~/.bashrc
$ julia --version
julia version 1.9.3

Add important packages
$ julia
julia> import Pkg
julia>Pkg.add(url="https://github.com/pmelsted/NetworkInference.jl")
julia>Pkg.add(“CSV”)
julia>Pkg.add(“DataFrames”)
julia>exit()

Proprocess the filtered (500 genes) gene expression matrix so the first row = sample names, first column = gene names
Produces: gene_expr_filtered_w_headers_T.tsv
$ python preprocess_expr_filteredT.py

Run PIDC
Produces: PIDC_inferred_network.txt
$ julia run_PIDC_filtered.jl
