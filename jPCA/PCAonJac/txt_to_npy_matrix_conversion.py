'''
Creates an .npy file from the .txt with the genotype matrix without NAs and values rounded to integers.
'''

import jPCA_settings
from jPCA_functions import *
import numpy as np

N = jPCA_settings.N
matrix_file = jPCA_settings.matrix_file #Original file to apply NAs_to_zeros on.
new_file_prefix = jPCA_settings.new_file_prefix #Prefix of file originated by NAs_to_zeros.

# Eliminate NAs:
NAs_to_zeros(matrix_file, new_file_prefix, N) # Uncomment to create file with no_NAs matrix.

# Import matrix to memory:
MATRIX = get_matrix(new_file_prefix, N)

# Round values to nearest integers:
MATRIX = np.rint(MATRIX)

# Save matrix as .npy file:
np.save('/hpc/hers_en/fsimoes/logs/objects/{}_N={}.npy'.format(new_file_prefix, N), MATRIX)
