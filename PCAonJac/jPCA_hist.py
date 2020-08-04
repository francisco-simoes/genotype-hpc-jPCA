'''
Create the histogram of jaccard values.
'''

import jPCA_settings
from jPCA_functions import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')

######################################################################
# Histogram to confirm Gaussianity
######################################################################
print("\n------ Histogram of generalized Jaccard scores---------")

#### Generalized Jaccard scores distribution
# We want to see if each entry J(i,j) is Gaussian distributed.
# We can use just a subset of the individuals.
#trial_number = 500 # Number of pairs of individuals to compare.

# Import similarity matrix:
N = jPCA_settings.N
sim_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N))

# Print imported sim matrix for debugging:
print('upper left corner imported sim matrix:', sim_matrix[:10,:10])
print('lower left corner imported sim matrix:', sim_matrix[-10:,-10:])

# NOTE: we expect J(i,j) to be Gaussian distributed and we can just use our entire population to see this because we assume that each person is the result of the same "rolls" (same probabilities for the snips).
# In other words we can assume that J(i,j) and J(i',j') follow the same distribution.

flat_sim_matrix = np.ndarray.flatten(sim_matrix) # Reduce to 1D.

# Histogram of the scores:
plt.figure()
plt.hist(flat_sim_matrix)
plt.title('Generalized Jaccard scores for N={}'.format(N))
plt.savefig('/hpc/hers_en/fsimoes/logs/images/Histogram_Jaccard_scores_for_N={}.png'.format(N))
#plt.show()

##########################################
## If using genotype matrix directly:
##########################################

#### Generalized Jaccard scores distribution
## We want to see if each entry J(i,j) is Gaussian distributed.
## We can use just a subset of the individuals.
##trial_number = 500 # Number of pairs of individuals to compare.
#
#
#trial_number = 40 # Number of pairs of individuals to compare.
#
#if trial_number > pop_size/2:
#    print("WARNING: It will fail because trial_number > half the population")
#
## Notice WE ARE NOT COMPUTING ALL THE J(I,J) FOR THIS HISTOGRAM: it would probably be overkill - we expect to see a Gaussian curve appear anyway.
#set1 = genotype_matrix[:trial_number,:]
#set2 = genotype_matrix[trial_number:2*trial_number,:]
#scores = []
#for i in range(trial_number):
#    individual_1 = set1[i]
#    individual_2 = set2[i]
#    score = generalized_jaccard_score(individual_1, individual_2)
#    scores += [score]
