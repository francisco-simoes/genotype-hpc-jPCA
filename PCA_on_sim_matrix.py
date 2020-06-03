'''
Run PCA on Jaccard matrix.
'''

import jPCA_settings
from jPCA_functions import *
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.preprocessing import scale

#plt.ion() # script will continue running after show().
plt.style.use('seaborn-white')

# Import settings and similarity matrix:
N = jPCA_settings.N
MATRIX = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_matrix_N={}.npy'.format(N))
print('Similarity matrix shape:', MATRIX.shape)

# Create dataframe
columns_list = ['similarity_with_individual_{}'.format(i) for i in range(MATRIX.shape[1])] # One individual (and thus one similarity index) for each column.
df = pd.DataFrame(MATRIX, columns = columns_list)

# Check df is in accordance with matrix.
print('Matrix corner:\n{}'.format(np.matrix(MATRIX[:4,:4])))
print('Data corner:\n{}'.format(df.iloc[:4,:4]))
# Basic (corner) data info.
print('\n\nData description:\n{}'.format(df.iloc[:,:5].describe()))

# Scaling: Must scale data before PCA (mean 0, std dev 1 along each feature (axis 0)).
scaled_df = pd.DataFrame(scale(df, axis=0), index=df.index, columns=df.columns)
print('\n\nScaled data description:\n{}'.format(scaled_df.iloc[:,:5].describe()))

# Fit PCA
#Each PC has a loading vector: a p-vector of normalized linear combination coefficients, where p is the number of variables.
#There are min(p, n-1) PCs, where n = {# of samples}.
#In this case, then: {# PCs} = 100-1.
#
#Get loading vectors: 
loadings_matrix = PCA().fit(scaled_df).components_.T #Each column contains one loading vector.
print(loadings_matrix.shape)
# ???: Shouldn't it be (..., 99) instead of (..., 100)?

loading_vectors_list = ['phi_{}'.format(i+1) for i in range(loadings_matrix.shape[1])]
loadings = pd.DataFrame(loadings_matrix, index=df.columns, columns=loading_vectors_list)
print('\n\nLoading vectors:\n{}'.format(loadings))


# Get PC scores:
#(The PC scores give us the projections of the data points onto the PCs).
pc_scores_list = ['PC{}_score'.format(i+1) for i in range(loadings_matrix.shape[1])]
scores_matrix = PCA().fit_transform(scaled_df) # One row for each sample; one column for each PC.
scores = pd.DataFrame(scores_matrix, index=scaled_df.index, columns=pc_scores_list)
print('\n\nScores (head):\n{}'.format(scores.head()))


# Visualize results using PC1 and PC2
fig, ax1 = plt.subplots(figsize=(9,9))

PC1_min = min(scores.PC1_score)
PC1_max = max(scores.PC1_score)
PC2_min = min(scores.PC2_score)
PC2_max = max(scores.PC2_score)

#ax1.set_xlim(PC1_min, PC1_max); ax1.set_ylim(PC2_min, PC2_max)
ax1.set_xlabel('PC1'); ax1.set_ylabel('PC2')
plt.title('First two PCs for N={}'.format(N))

#Create scatter plot:
plt.scatter(scores.PC1_score, scores.PC2_score)
plt.savefig('/hpc/hers_en/fsimoes/logs/images/PCs_N={}.png'.format(N))
#plt.show()


# Explained variance plot
fitted = PCA().fit(scaled_df)
print('\n\nPVEs:\n{}'.format(fitted.explained_variance_ratio_))

plt.figure(figsize=(7,7))

PCs = np.arange(1, len(fitted.explained_variance_ratio_)+1)
plt.plot(PCs, fitted.explained_variance_ratio_, '-', label='Proportion of explained variance (PVE)')
plt.plot(PCs, np.cumsum(fitted.explained_variance_ratio_), '-', label='Cumulative proportion of explained variance')

plt.ylabel('Proportion of Variance Explained')
plt.xlabel('Principal Component')
plt.xlim(0.75, len(fitted.explained_variance_ratio_)+0.25)
plt.ylim(0,1.05)
plt.xticks(PCs)
plt.legend(loc=2);
plt.title('PVE plots using N={} samples'.format(N))

plt.savefig('/hpc/hers_en/fsimoes/logs/images/PVE_N={}'.format(N))
#plt.show()

