# BMI_776_Project

## Project Description
We compared the Gene Co-Expression Network (GCN) inference algorithms: GENIE3, GRNBoost2, PIDC. *Note: While the algorithms are generally referred to as Gene Regulatory Network (GRN) inference algorithms, we did not use any information regarding transcription factors, so all interactions were predicted purely based on gene expression (and therefore co-expression) information.*

## Description of Folders and Files
Below describes the directories and some of the files contained within our project repository. We briefly describe each script and notebook used in our project, but do not expand upon all pickle or CSV files used in our analyses.

### Code/
Files in the `Code/` directory include our data processing, BioGRID testing files, and several files used for intermediate steps in our pipeline.

#### BioGRID_Test.py
`BioGRID_Test.py` takes the predicted interactions from each method (GENIE3, GRNBoost2, and PIDC) and queries the BioGRID database to check if the gene interactions are experimentally validated.

#### data_preprocessing.ipynb
`data_preprocessing.ipynb` processes the RNA-seq data and filters the genes to give us our top 500 most highly variable genes.

#### Ensembl_Conversions.ipynb
`Ensembl_Conversions.ipynb` queries the Ensembl REST API to create a mapping between Ensembl IDs used by our original dataset and commonly used gene names. These gene names are then used when querying the BioGRID API.

#### run_genie3_grnboost2.py
`run_genie3_grnboost2.py` provides a script to run one or both of the network inference algorithms (GENIE3 and/or GRNBoost2) and outputs a ranked list of gene interactions.

#### venn_diagram.ipynb
`venn_diagram.ipynb` generates the Venn diagrams for shared gene interactions (network edges) and verified interactions between the three network inference algorithms.

### Data/SARS-CoV-2/
Contains all raw data files and intermediate files for further analyses, such as the dictionary mappings from Ensembl IDs to gene names.

### GENIE3/
Submodule created using the original GitHub repository associated with the original GENIE3 paper.
The GENIE3_python/ subdirectory was used for our project.

### GRNBoost2/
Contains code related to running GRNBoost2. This code is slightly redundant, as `run_genie3_grnboost2.py` also has this capability.

#### run_GRNBoost2_filtered.py
`run_GRNBoost2_filtered.py` runs GRNBoost2 on our filtered genes (top 500 most highly variable).

### PIDC/
Contains code related to running PIDC.

#### preprocess_expr_filteredT.py
`preprocess_expr_filteredT.py` prepares gene expression data for PIDC.

#### run_PIDC_filtered.jl
`run_PIDC_filtered.jl` runs the PIDC algorithm.

### Results/
Contains results and code, including ranked interaction lists and the code required to make the adjacency matrices and undirected graphs.

#### Results/Undirected_Results/
Contains code related to generating and analyzing the undirected graphs corresponding to the gene interaction lists made by running the network inference algorithms.

##### convert2geneID_pickle.py
`convert2geneID_pickle.py` converts the results from each network inference algorithm to use gene names instead of Ensembl IDs.

##### make_undirected.py
`make_undirected.py` makes the ranked interaction list undirected by removing duplicate interactions

#### Results/Undirected_Results/adjecency_matrices/
Contains code for creating and analyzing adjacency matrices.

##### adj_matrices.ipynb
`adj_matrices.ipynb` creates adjacency matrices for results and analyzes them with Spearman and Pearson correlations. It also creates heatmaps for the co-expression data.

##### adj_matrix.py
`adj_matrix.py` creates adjacency matrices for results.

### Sandbox/
All files in the Sandbox folder were used to develop and explore code. There are non-essential for our pipeline.
