import pandas as pd
import numpy as np
import pickle
import scanpy as sc
from matplotlib import pyplot as plt
import sys

# Imports for Algos
sys.path.append('../GENIE3/GENIE3_python/')
from GENIE3 import GENIE3, get_link_list
from arboreto.algo import grnboost2

### Specify configuration
data_path = '../Data/highly_variable_expression_matrix_503.pickle'
gene_names_path = '../Data/highly_variable_genes_503.pickle'

def print_usage():
    # Print usage of script for user
    print('Running run_genie3_grnboost2.py')
    print('Usage: python run_genie3_grnboost2.py <algo: \"GENIE3\" or \"GRNBoost2\">')
    print('If <algo> is not specified, both GENIE3 and GRNBoost2 are run.')


def run_genie3(data_path, gene_names_path):
    """
    Runs GENIE3 algorithm.
    Returns 
    
    Params:
    data_path: file path to gene expression matrix
    gene_names_path: file path to list of genes used in expression matrix (in order)
    """
    
    # Load data
    with open(data_path, 'rb') as f:
        data = pickle.load(f)

    # Get gene names
    with open(gene_names_path, 'rb') as f:
        gene_names = pickle.load(f)
        num_genes = len(gene_names)
        
    # #### Testing on just 10 genes
    # data = data[:, :10]
    # print('data.shape: ', data.shape)
    # gene_names = gene_names[:10]
    # num_genes = len(gene_names)
    

    # Run GENIE3 to get regulatory link scores matrix 
    # M(i,j) is the weight of link from i-th gene to j-th gene
    M = GENIE3(data, gene_names=gene_names)
    print(M)

    # Output resulting matrix
    with open(f'../Results/GENIE3/reg_link_matrix_{num_genes}.pickle', 'wb') as f:
        pickle.dump(M, f)

    # Get list of ranked predictions
    ranked_preds = get_link_list(M, 
                                 gene_names=gene_names, 
                                 file_name=f'../Results/GENIE3/ranked_interaction_list_{num_genes}.pickle')

    return
    

# For Livvy
def run_grnboost2():
    """
    Run GRNBoost2 algorithm
    """
    print('hi')
    return
    

if __name__ == "__main__":
    print_usage()
    # Check for args. If none, run both GRN algorithms
    args = sys.argv
    if len(args) == 1:
        print('Running both GENIE3 and GRNBoost2.')
    elif len(args) == 2:
        algo = args[1]
        print(f'Running {algo}')

        # Run algo
        if algo == 'GENIE3':
            run_genie3(data_path, gene_names_path)
        elif algo == 'GRNBoost2':
            run_grnboost2()
        
    else:
        print('Incorrect number of arguments. No algorithms will be run.')
    
    