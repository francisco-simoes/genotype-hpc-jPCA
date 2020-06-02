'''
Import genotype matrix using functions from jPCA_functions.py and create the jaccard similarity matrix.
Save it as a .npy file.
Also generates a heatmap representation of the matrix.
'''

import jPCA_settings
from jPCA_functions import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')

######################################################################
# Import and preprocess data
######################################################################

## Get matrix
print("\n------ Importing the genotype matrix ---------")

# Matrix has 12803 columns (genes) and 30821 rows (30820 individuals and the first row has the gene names; 12802 burdens and the first column has sample tags).
#       (Numbers obtained by simply running ```head --lines=1 indiv_counts_LOF_maf001_exQCpass_merged.txt | wc``` and ```wc -l indiv_counts_LOF_maf001_exQCpass_merged.txt```.)

# Needed parameters from settings file
N = jPCA_settings.N
new_file_prefix = jPCA_settings.new_file_prefix

# Loading the matrix, already rounded and without NAs.
MATRIX = np.load('/hpc/hers_en/fsimoes/logs/objects/{}_N={}.npy'.format(new_file_prefix, N))
print('Matrix shape:', MATRIX.shape)

## Create dataframe
columns_list = ['gene_{}'.format(i) for i in range(MATRIX.shape[1])] # One gene for each column.
df = pd.DataFrame(MATRIX, columns = columns_list)

# Check df is in accordance with matrix.
print('Matrix corner:\n{}'.format(np.matrix(MATRIX[:4,:4])))
print('Data corner:\n{}'.format(df.iloc[:4,:4]))
# Basic (corner) data info.
description = df.describe()
print('\n\nData description:\n{}'.format(description))
print( '\n\nMin matrix value: {}, Max matrix value: {}'.format(description.loc['min',:].min(), description.loc['max',:].max()) )

######################################################################
# Construct the generalized Jaccard matrix
######################################################################
print("\n------ Constructing the (generalized) Jaccard matrix ---------")

genotype_matrix = MATRIX # Just a convenient change of names.
print('Genotype matrix:\n',genotype_matrix)

# We now compute the generalized Jaccard scores between all individuals, obtaining a similarity matrix.
pop_size = genotype_matrix.shape[0]
sim_matrix = np.zeros((pop_size, pop_size))
for i in range(pop_size):
    for j in range(i,pop_size): # Since the matrix is symmetric, we only need to compute for j>=1.
        individual_i = genotype_matrix[i,:]
        individual_j = genotype_matrix[j,:]
        sim_matrix[i,j] = generalized_jaccard_score(individual_i, individual_j)
        sim_matrix[j,i] = sim_matrix[i,j] # Matrix is symmetric.

plt.figure()
plt.imshow(sim_matrix, cmap='hot')
plt.colorbar()
plt.title('Similarity matrix colormap with N={}'.format(N))
plt.savefig('/hpc/hers_en/fsimoes/logs/images/Generalized_Jaccard_scores_matrix_N={}.png'.format(N))
#plt.show()

# Save the similarity matrix in a file.
np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N), sim_matrix)

# Print corners of similarity matrix for debugging:
print('Upper left OG sim matrix corner:', sim_matrix[:10,:10])
print('Lower right OG sim matrix corner:', sim_matrix[-10:,-10:])
