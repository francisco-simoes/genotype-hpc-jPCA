'''
Dividing the histogram in three sections (the "zero section" and the two peaks), count how many individuals belong to each pheno on each section of the histogram.
The result is a list of dictionaries with entries pheno:frequency, one for each section, which is printed and saved in a pickle file.
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
phenos = df['pheno'].unique()
number_of_phenos = len(phenos)
print('Phenos:', df['pheno'].unique())

# Count frequency of each pheno in each of the three histogram sections.
#section1 = [0, 0.001[; section2 = [0.001, 0.01[; section3 = [0.01, 0.03]
delimiters = [0, 0.001, 0.01, 0.03]
#make list of zeros and iterable to feed to the dictionaries:
zeros_list = [0] * number_of_phenos
iterable = list(zip(phenos, zeros_list)) # List of type [(pheno, 0), ...]
section_phenos = [ dict(iterable), dict(iterable), dict(iterable) ]

for i in range(sim_matrix.shape[0]):
    for j in range(sim_matrix.shape[1]):
#        print(i,j)
#        print(df['pheno'][i], df['pheno'][j])
#        print(sim_matrix[i,j])
        if i <= j: #only need to use these cases since the matrix is symmetric.
            if delimiters[0] <= sim_matrix[i,j] < delimiters[1]: #if J(i,j) is in the first section.
                section_phenos[0][df['pheno'][i]] += 1
                section_phenos[0][df['pheno'][j]] += 1
            if delimiters[1] <= sim_matrix[i,j] < delimiters[2]: #if J(i,j) is in the second section.
                section_phenos[1][df['pheno'][i]] += 1
                section_phenos[1][df['pheno'][j]] += 1
            if delimiters[2] <= sim_matrix[i,j] <= delimiters[3]: #if J(i,j) is in the third section.
                section_phenos[2][df['pheno'][i]] += 1
                section_phenos[2][df['pheno'][j]] += 1

for i in range(len(section_phenos)):
    print('\nPhenos in section {}:'.format(i), section_phenos[i])

# Save the resulting list of dictionaries in a pickle file.
with open('/hpc/hers_en/fsimoes/logs/objects/section_phenos_dicts.pkl', 'wb') as file:
    pickle.dump(section_phenos, file, pickle.HIGHEST_PROTOCOL)
