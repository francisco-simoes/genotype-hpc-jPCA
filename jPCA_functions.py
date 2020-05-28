'''
Functions to prepare the genotype data for jPCA.
'''

import numpy as np

######################################################################
# Functions
######################################################################
def generalized_jaccard_score(a1, a2): # From the Jaccard Gaussian simulation I did before.
    '''
    Computes the ratio {# entries where (a1 and a2 agree) and (a1 and a2 are positive)} / {# entries where either a1 or a2 are positive (or both)}. 

    Parameters
    --------
    a1, a2: arrays to compare.

    Returns
    --------
    ratio: real value in [0, 1].
    '''
    bool_a1, bool_a2, bool_intersect = a1!=0, a2!=0, a1==a2
    # Number of indices where both arrays are equal and nonzero:
    positive_intersection = np.count_nonzero(bool_a1 & bool_intersect) # & uses and on each array index.
    # (Only need to check one of them is positive, since the entries are equal at the sites of interest).

    # Number of positive entries:
    positive_total = np.count_nonzero(bool_a1 | bool_a2) # | uses or on each array index.

    # The score:
    if positive_total == 0: # If there are no positive entries where a1 and a2 coincide: set J to 0.
        ratio = 0
    else:
        ratio = positive_intersection / positive_total
    return ratio

# Function to remove NAs and select only some rows. Also eliminated the first row (with the gene names).
def NAs_to_zeros(matrix_file, new_file_prefix, N): # Similar to the function I used on the toy data.
    '''
    Creates a file named '<new_file_prefix>_N='N'.txt' from 'matrix_file', containing the first N lines of the matrix and with NAs replaced by zeros. Eliminates the first line and first column.
    --------------
    Returns: None
    '''
    # Save the first N lines in a list.
    with open(matrix_file, 'r') as original_file:
        first_lines = [next(original_file) for i in range(N+1)] # N+1 because we'll delete the first row.
    # Eliminate first row from the list:
    first_lines = first_lines[1:]
    # Eliminate first element (word) from each line (row). (They are tags for the samples).
    for i,line in enumerate(first_lines):
            first_lines[i] = line.split("\t",1)[1] # Eliminates first word (until the first tab \t).

    # Create file with the first N lines of the matrix, with NAs replaced by 0s.
    new_file = open('{}_N={}.txt'.format(new_file_prefix, N), 'w') # Create file, or empty it if it already exists.
    for line in first_lines:
        new_line = line.replace('NA', '0')
        new_file.write(new_line) # Append line to bottom of new_file.
    new_file.close()
    return

# Function to extract matrix for given N, using the file from the function above.
def get_matrix(new_file_prefix, N): # Similar to the function I used on the toy data.
    '''
    Creates a matrix with the first N lines of the original matrix_file.
    The file with the matrix must have been previously created using the function NAs_to_zeros.
    ------------
    Returns: MATRIX - a numpy array with the first N lines of the matrix, with the NAs removed.
    '''
    MATRIX = np.loadtxt('{}_N={}.txt'.format(new_file_prefix, N))
    return MATRIX

