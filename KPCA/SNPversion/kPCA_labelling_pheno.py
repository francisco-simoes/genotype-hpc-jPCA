print(f'START of {__file__}')

import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import jPCA_settings
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #Won't need X display.
import matplotlib
import matplotlib.pyplot as plt

# Load necessary settings
#N = jPCA_settings.N

# Get labels' dataframe
df = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
#df = df.iloc[:N]
#print(df)
print(df.columns)
phenos = df['pheno'].unique()
number_of_phenos = len(phenos)
print('Phenos:', df['pheno'].unique())

# Load the PC scores and create scores Dataframe.
#scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca.npy')
#scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common.npy')
scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common_alternative_VAR.npy')
#(One PC for each column).

# Plot with colored classes
x = scores_matrix[:,0]
y = scores_matrix[:,1]
#Need 2 colors.
colors = ['green', 'red']
labels = df['pheno'].factorize()[0]

fig = plt.figure(figsize=(8,8))
plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
cb = plt.colorbar()
loc = np.arange(0,max(labels),max(labels)/float(len(colors)))
cb.set_ticks(loc)
cb.set_ticklabels(phenos)
plt.title('kpca: First two PCs for SNP burdens; pheno labels')
plt.xlabel('PC1')
plt.ylabel('PC2')
#plt.savefig('/hpc/hers_en/fsimoes/logs/images/kPCA_pheno_colorized_SNP_common.png')
plt.savefig('/hpc/hers_en/fsimoes/logs/images/kPCA_pheno_colorized_SNP_common_alternative_VAR.png')
#plt.show()

print(f'END of {__file__}')
