'''
Run KPCA on genotype matrix using Jaccard score as the kernel.
Needs the Gram matrix (i.e. similarity matrix) to have been previously computed.
Plots PC1 and PC2.
'''

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
nvars=500000

from sklearn.decomposition import PCA, KernelPCA

#plt.ion() # script will continue running after show().
plt.style.use('seaborn-white')

GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_eur_rare_with_{}_vars.txt'.format(nvars))
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
X_kpca = kpca.fit_transform(df) #This is the scores matrix! fit_transform already centers the Gram matrix.
print('X_kpca shape: ', X_kpca.shape)

pc_scores_list = ['PC{}_score'.format(i+1) for i in range(X_kpca.shape[1])]

#Save it in .npy file.
np.save('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_eur_rare_mine_with_{}_vars.txt'.format(nvars), X_kpca)

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
plt.title('kPCA: First two PCs for SNP burdens.')
#Create scatter plot:
plt.scatter(scores.PC1_score, scores.PC2_score)
plt.savefig('/hpc/hers_en/fsimoes/logs/images/kPCA_PCs_eur_rare_mine_with_{}_vars.png'.format(nvars))
#plt.show()
