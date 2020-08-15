import numpy as np
from sklearn.metrics import jaccard_score
from scipy.stats import binom
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')

# We want to extend this to other positive integers.
def generalized_jaccard_score(a1, a2):
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


# main

######################################################################
# Test generalized_jaccard_score:
######################################################################
print("\n------ Testing generalized_jaccard_score ---------")

# The jaccard_score gives {# entries with same value 1}/{# entries with at least one value 1}
# So the two functions should coincide for these a, b:
a = np.array([1, 0, 0, 1, 0, 0])
b = np.array([0, 1, 0, 1, 0, 0])
print("\na:", a, "\nb:", b)
print( "generalized_jaccard_score(a,b): {} \njaccard_score(a,b): {}".format(generalized_jaccard_score(a, b), jaccard_score(a,b)) )

# General case
c = np.array([2, 0, 1, 5, 0, 7])
d = np.array([0, 0, 1, 1, 0, 7])
print("\nc:", c, "\nd:", d)
print( "generalized_jaccard_score(c,d): {}".format(generalized_jaccard_score(c, d)) )

print("It works!!")


######################################################################
# Are Jaccard scores Gaussian when the data is binomial (with same n=2 but different p)?
######################################################################
print("\n------ Visualizing the generalized Jaccard scores distribution ---------")

#### First we generate a couple of binomial samples and see what they look like.
print("\n Binomial distribution - examples")
####FDG
n = 2
p1 = 0.1
p2 = 0.4
np.random.seed(0)
sample1 = binom.rvs(n, p1, size=1000)
sample2 = binom.rvs(n, p2, size=1000)

fig, ax = plt.subplots(2)
ax[0].hist(sample1, bins=n+1)
ax[1].hist(sample2, bins=n+1)
ax[0].set_title('B$(n={}, p={})$'.format(n, p1) )
ax[1].set_title('B$(n={}, p={})$'.format(n, p2) )
plt.show()

#### Population simulation:
# Now the idea is that each pair of individuals (samples) has one binomially distributed
#burden in {0, 1, 2} for each SNP s_i, with Binomial parameters n=2, p=p_i.
# Let's generate (simulate) the population:

print("\n Population simulation")
n = 2
snip_number = 1000
pop_size = 1010

np.random.seed(0)
probs = np.random.rand(snip_number,)/2 # vector of randomized probabilities < 0.5 (minor alleles).
# (Same probs for every individual!)
genotype_matrix = np.zeros((pop_size, snip_number))
for k in range(pop_size): # Generate pop_size individuals.
    burdens = [] # Initialize the burdens of the individual k.
    for p_i in probs: # Generate the burdens of the individual k.
        burdens += [binom.rvs(n, p_i)] # add one binomially distributed burden.
    genotype_matrix[k,:] = np.array(burdens) # One row for each individual/sample.

print('Genotype matrix:\n',genotype_matrix)

print("\n------ Similarity matrix and histogram of generalized Jaccard scores---------")
#### Similarity matrix
# We now compute the generalized Jaccard scores between all individuals, obtaining a similarity matrix.
print("\n Similarity matrix")
sim_matrix = np.zeros((pop_size, pop_size))
for i in range(pop_size):
    for j in range(i, pop_size): # Since the matrix is symmetric, we only need to compute for j>=1.
        individual_i = genotype_matrix[i,:]
        individual_j = genotype_matrix[j,:]
        sim_matrix[i,j] = generalized_jaccard_score(individual_i, individual_j)
        sim_matrix[j,i] = sim_matrix[i,j] # Matrix is symmetric.

print('hre', sim_matrix[5:10, 5:10])
plt.figure()
plt.imshow(sim_matrix, cmap='hot')
plt.colorbar()
plt.title(f'Similarity matrix colormap for population simulation with {snip_number} SNPs and {pop_size} individuals; randomized AFs < 0.5')
plt.show()

#### Generalized Jaccard scores distribution
# We want to see if each entry J(i,j) is Gaussian distributed.
# We could generate two individuals many times (always with the same Bernoulli probabilities) and compute their score each time.
# Instead, we will simply use the individuals that we already generated above.
trial_number = 500 # Number of pairs of individuals to compare.

if trial_number > pop_size/2:
    print("It will fail because trail_number > half size of generated population")

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
plt.title(f'Generalized Jaccard scores for {trial_number} compared individuals and {snip_number} SNPs')
plt.savefig(f'Generalized_Jaccard_scores_for_{trial_number}_compared_individuals_and_{snip_number}_SNPs')
plt.show()
