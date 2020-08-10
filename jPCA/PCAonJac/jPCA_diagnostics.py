'''
Prints useful values to diagnose problems with the genotype matrix.
'''
print('------------ Diagnosis ------------------')

import jPCA_settings
import numpy as np

# Import settings:
N = jPCA_settings.N
#N = 30820
new_file_prefix = jPCA_settings.new_file_prefix
NOT_rounded_new_file_prefix = jPCA_settings.NOT_rounded_new_file_prefix

# Import rounded and NOT rounded genotype matrices:
MATRIX = np.load('/hpc/hers_en/fsimoes/logs/objects/{}_N={}.npy'.format(new_file_prefix, N))

not_rounded_MATRIX = np.load('/hpc/hers_en/fsimoes/logs/objects/{}_N={}.npy'.format(NOT_rounded_new_file_prefix, N))

# Number of non-zeros in the rounded and NOT rounded matrices
positive_count = np.count_nonzero(MATRIX)
NOT_rounded_positive_count = np.count_nonzero(not_rounded_MATRIX)


# Percentages of zeros
total_count = MATRIX.size #Number of matrix elements
positive_ratio = positive_count/total_count
NOT_rounded_positive_ratio = NOT_rounded_positive_count/total_count

print('Ratio of zeros in rounded matrix: ', 1 - positive_ratio)
print('Ratio of zeros in NOT rounded matrix: ', 1 - NOT_rounded_positive_ratio)
print('Number of values coming from non-zero mean-imputation: ', NOT_rounded_positive_count - positive_count)
print('(The above number is correct if, as it seems to be in this case, the mean of every gene burden is close to zero, thus being rounded to zero)')


# Number of zeros in the rounded Jaccard matrix
sim_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N))
print('Number of zeros in rounded Jaccard matrix:', sim_matrix.size - np.count_nonzero(sim_matrix))
print('Number of total elements in the Jaccard matrix:', sim_matrix.size)
