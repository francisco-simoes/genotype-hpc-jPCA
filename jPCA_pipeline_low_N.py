'''
jPCA for the gene-burden genotype matrices.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')

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

######################################################################
# Import and preprocess data
######################################################################

## Get matrix
print("\n------ Importing the genotype matrix ---------")

# Matrix has 12803 columns (genes) and 30821 rows (30820 individuals and the first row has the gene names; 12802 burdens and the first column has sample tags).
#       (Numbers obtained by simply running ```head --lines=1 indiv_counts_LOF_maf001_exQCpass_merged.txt | wc``` and ```wc -l indiv_counts_LOF_maf001_exQCpass_merged.txt```.)

# [ADAPT THIS TO THE FILE YOU WANT TO USE]
#N = 30820 # Use all rows.
N = 100
matrix_file = '/hpc/hers_en/fsimoes/jPCA/indiv_counts_LOF_maf001_exQCpass_merged.txt'
new_file_prefix = 'No_NAs_LOF_matrix'

#NAs_to_zeros(matrix_file, new_file_prefix, N) # Uncomment to create file with no_NAs matrix.
MATRIX = get_matrix(new_file_prefix, N)
print('Matrix shape:', MATRIX.shape)

## Create dataframe
columns_list = ['gene_{}'.format(i) for i in range(MATRIX.shape[1])] # One gene for each column.
df = pd.DataFrame(MATRIX, columns = columns_list)

# Check df is in accordance with matrix.
print('Matrix corner:\n{}'.format(np.matrix(MATRIX[:4,:4])))
print('Data corner:\n{}'.format(df.iloc[:4,:4]))
# Basic (corner) data info.
print('\n\nData description:\n{}'.format(df.iloc[:,:5].describe()))

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
plt.title('Similarity matrix colormap')
plt.show()

# Save the similarity matrix in a file.
np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N), genotype_matrix)

######################################################################
# Histogram to confirm Gaussianity
######################################################################
print("\n------ Histogram of generalized Jaccard scores---------")

#### Generalized Jaccard scores distribution
# We want to see if each entry J(i,j) is Gaussian distributed.
# We can use just a subset of the individuals.
#trial_number = 500 # Number of pairs of individuals to compare.
trial_number = 40 # Number of pairs of individuals to compare.

if trial_number > pop_size/2:
    print("It will fail because trial_number > half the population")

# Notice WE ARE NOT COMPUTING ALL THE J(I,J) FOR THIS HISTOGRAM: it would probably be overkill - we expect to see a Gaussian curve appear anyway.

# Create two sets of individuals (i.e. their burden vectors).
# We will compare individuals of set1 with individuals of set2, without repeating.
set1 = genotype_matrix[:trial_number,:]
set2 = genotype_matrix[trial_number:2*trial_number,:]
scores = []
for i in range(trial_number):
    individual_1 = set1[i]
    individual_2 = set2[i]
    score = generalized_jaccard_score(individual_1, individual_2)
    scores += [score]

# Histogram of the scores:
plt.figure()
plt.hist(scores)
plt.title('Generalized Jaccard scores for {} trials, file={}'.format(trial_number, matrix_file))
plt.savefig('/hpc/hers_en/fsimoes/logs/images/Generalized_Jaccard_scores_for_{}_trials.png'.format(trial_number))
plt.show()
# NOTE: we expect J(i,j) to be Gaussian distributed and we can just use our population to see this because we assume that each person is the result of the same "rolls" (same probabilities for the snips). 

######################################################################
# PCA on the generalized Jaccard scores
######################################################################


######################################################################
# The gene-burdens case
######################################################################
# The same, but now the burdens must be generated by pseudo-binomial distributions with varying Bernoulli trials, and maybe even some dependence of variables... Must know the form of this dependency!




