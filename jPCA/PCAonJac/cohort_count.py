'''
Dividing the histogram in three sections (the "zero section" and the two peaks), count how many individuals belong to each cohort on each section of the histogram.
The result is a list of dictionaries with entries cohort:frequency, one for each section, which is printed and saved in a pickle file.
'''

import pickle
import jPCA_settings
import pandas as pd
import numpy as np

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

# Save the resulting list of dictionaries in a pickle file.
#section_cohorts = [ {'nan': 339365691, 'Netherlands': 41711094, 'Belgium': 11188425, 'Ireland': 10733899, 'UK': 30196418, 'Spain_Madrid': 5651105, 'US': 7387462, 'NYGC': 10087947, 'Spain_Barcelona': 2204244, 'Portugal': 1028293, 'Sweden': 3338244, 'Swiss': 787645, 'France': 4342614, 'Turkey': 1576796, 'Israel': 731106, 'Italy': 966045}, {'nan': 231469674, 'Netherlands': 28261568, 'Belgium': 7594069, 'Ireland': 7136554, 'UK': 20354975, 'Spain_Madrid': 3853861, 'US': 4963708, 'NYGC': 6923468, 'Spain_Barcelona': 1571924, 'Portugal': 705843, 'Sweden': 2232815, 'Swiss': 553111, 'France': 3001343, 'Turkey': 1142938, 'Israel': 519758, 'Italy': 663643}, {'nan': 104734501, 'Netherlands': 12795222, 'Belgium': 3406137, 'Ireland': 3187051, 'UK': 9137246, 'Spain_Madrid': 1726629, 'US': 2235061, 'NYGC': 3206073, 'Spain_Barcelona': 726882, 'Portugal': 306148, 'Sweden': 1013553, 'Swiss': 263530, 'France': 1371206, 'Turkey': 552773, 'Israel': 243657, 'Italy': 296103} ]

with open('/hpc/hers_en/fsimoes/logs/objects/section_cohorts_dicts.pkl', 'wb') as file:
    pickle.dump(section_cohorts, file, pickle.HIGHEST_PROTOCOL)
