'''
Dividing the histogram in three sections (the "zero section" and the two peaks), count how many individuals belong to each cohort on each section of the histogram.
'''

import jPCA_settings
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Load necessary settings
N = jPCA_settings.N

# Import similarity matrix
sim_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N))
#flat_sim_matrix = np.ndarray.flatten(sim_matrix) # Reduce to 1D.

# Create labels' dataframe
df = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
df = df.iloc[:N]
#print(df)
#print(df.columns)
print('# of non-NA cohorts:', len(df['cohort']) - df['cohort'].count())
cohorts = df['cohort'].unique()
number_of_cohorts=len(cohorts)
print('Cohort types:', df['cohort'].unique(), '\nTotal number of cohort types:', number_of_cohorts)

# Count cohorts of each of the three histogram sections.
#section1 = [0, 0.001[; section2 = [0.001, 0.01[; section3 = [0.01, 0.03]
delimiters = [0, 0.001, 0.01, 0.03]
#make list of zeros and iterable to feed to the dictionaries:
zeros_list = [0] * number_of_cohorts
iterable = list(zip(cohorts, zeros_list)) # List of type [(cohort, 0), ...]
section_cohorts = [ dict(iterable), dict(iterable), dict(iterable) ]

for i in range(sim_matrix.shape[0]):
    for j in range(sim_matrix.shape[1]):
#        print(i,j)
#        print(df['cohort'][i], df['cohort'][j])
#        print(sim_matrix[i,j])
        if i <= j: #only need to use these cases since the matrix is symmetric.
            if delimiters[0] <= sim_matrix[i,j] < delimiters[1]: #if J(i,j) is in the first section.
                section_cohorts[0][df['cohort'][i]] += 1
                section_cohorts[0][df['cohort'][j]] += 1
            if delimiters[1] <= sim_matrix[i,j] < delimiters[2]: #if J(i,j) is in the second section.
                section_cohorts[1][df['cohort'][i]] += 1
                section_cohorts[1][df['cohort'][j]] += 1
            if delimiters[2] <= sim_matrix[i,j] <= delimiters[3]: #if J(i,j) is in the third section.
                section_cohorts[2][df['cohort'][i]] += 1
                section_cohorts[2][df['cohort'][j]] += 1

for i in range(len(section_cohorts)):
    print('\nCohorts in section {}:'.format(i), section_cohorts[i])
