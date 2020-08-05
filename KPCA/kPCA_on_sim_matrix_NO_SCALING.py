'''
Run KPCA on genotype matrix using Jaccard score as the kernel.
Needs the Gram matrix (i.e. similarity matrix) to have been previously computed.
'''
print(f'START of {__file__}')

import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import jPCA_settings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from sklearn.preprocessing import scale
from jPCA_functions import *
from sklearn.decomposition import PCA, KernelPCA
from sklearn.datasets import make_circles

#plt.ion() # script will continue running after show().
plt.style.use('seaborn-white')

# Import settings and similarity matrix:
N = jPCA_settings.N
n_components = jPCA_settings.n_components
GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N))
print('Similarity matrix shape:', GRAM.shape)

# Create dataframe
columns_list = ['similarity_with_individual_{}'.format(i) for i in range(GRAM.shape[1])] # One individual (and thus one similarity index) for each column.
df = pd.DataFrame(GRAM, columns = columns_list)

#Check df is in accordance with matrix.
print('Matrix corner:\n{}'.format(np.matrix(GRAM[:4,:4])))
print('Data corner:\n{}'.format(df.iloc[:4,:4]))
# Basic (corner) data info.
print('\n\nData description:\n{}'.format(df.iloc[:,:5].describe()))

# Fit jPCA
kpca = KernelPCA(kernel='precomputed')
X_kpca = kpca.fit_transform(df) #This is the scores matrix!
print(X_kpca.shape)

pc_scores_list = ['PC{}_score'.format(i+1) for i in range(X_kpca.shape[1])]

#Save it in .npy file.
np.save('/hpc/hers_en/fsimoes/logs/objects/kPCA_X_kpca_N={}.npy'.format(N), X_kpca)

scores = pd.DataFrame(X_kpca, index=df.index, columns=pc_scores_list)
print('\n\nScores (head):\n{}'.format(scores.head()))


# Visualize results using PC1 and PC2
fig, ax1 = plt.subplots(figsize=(9,9))

PC1_min = min(scores.PC1_score)
PC1_max = max(scores.PC1_score)
PC2_min = min(scores.PC2_score)
PC2_max = max(scores.PC2_score)

#ax1.set_xlim(PC1_min, PC1_max); ax1.set_ylim(PC2_min, PC2_max)
ax1.set_xlabel('PC1'); ax1.set_ylabel('PC2')
plt.title('kPCA: First two PCs for N={}'.format(N))
#Create scatter plot:
plt.scatter(scores.PC1_score, scores.PC2_score)
plt.savefig('/hpc/hers_en/fsimoes/logs/images/kPCA_PCs_N={}.png'.format(N))
#plt.show()

print(f'END of {__file__}')
