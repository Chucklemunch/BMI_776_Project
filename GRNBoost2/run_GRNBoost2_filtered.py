# import necessary modules
import pandas as pd
from arboreto.algo import grnboost2
import pickle
import numpy as np

if __name__ == '__main__':
    # Load the data
    with open("highly_variable_expression_matrix_503.pickle", "rb") as f:
        obj = pickle.load(f)
    with open("highly_variable_genes_503.pickle", "rb") as f:
        genes = pickle.load(f)
    
    df_variable = pd.DataFrame(obj)
    df_variable.index=genes
    
    # Transpose (to be rows=samples, columns=genes)
    df_variable_T = df_variable.T

    # Run GRNBoost2 (infer co-expression network)
    network_grnboost2 = grnboost2(df_variable_T, tf_names=None, gene_names=genes)

    # Save the result to a file (GRNBoost2 returns a DataFrame)
    network_grnboost2.to_csv("GRNBoost2_network.csv", sep="\t", index=False)

    print(network_grnboost2.head())

