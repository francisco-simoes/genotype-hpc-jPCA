print(f'START of {__file__}')

'''
Check if kPCA pcs correlate with usual PCs.
'''
import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import jPCA_settings
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #Won't need X display.
import matplotlib.pyplot as plt

# Load necessary settings
#N = jPCA_settings.N

# Get OG pcs
df = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
#df = df.iloc[:N]
#print(df)
print(df.columns)

OG_pcs_df = df.iloc[:, 6:16]
OG_scores_matrix = OG_pcs_df.to_numpy()
print('OG scores matrix shape:', OG_scores_matrix.shape)

# Load the kpca PC scores
#kpca_scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca.npy')
#kpca_scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common.npy')
kpca_scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common_alternative_VAR.npy')
kpca_scores_matrix = kpca_scores_matrix[:, :10] 
print('kpca pc scores matrix shape:', kpca_scores_matrix.shape)
#(One PC for each column).


# Correlations heatmap
all_scores = np.concatenate((OG_scores_matrix, kpca_scores_matrix), axis=1)
corr_matrix = pd.DataFrame(all_scores).corr().to_numpy()
print(corr_matrix[:10, :])

fig, ax = plt.subplots(figsize=(10,10))
im = ax.imshow(corr_matrix)

#We want to show all ticks...
dim1 = corr_matrix.shape[0]
dim2 = corr_matrix.shape[1]
ax.set_xticks(range(dim1))
ax.set_yticks(range(dim2))

ax.set_xticklabels([i + 1 for i in range(dim1)])
ax.set_yticklabels([i + 1 for i in range(dim2)])

#Loop over data dimensions and create text annotations.
for i in range(dim1):
    for j in range(dim2):
        text = ax.text(j, i, round(corr_matrix[i, j], 2), ha="center", va="center", color="w")

ax.set_title("Correlation between kPCA PCs and standard PCs - SNP alternative vars case.")
fig.tight_layout()
plt.savefig('/hpc/hers_en/fsimoes/logs/images/kpca_vs_OG_correlation_SNP_common_alternative_VAR.png')
#plt.show()

print(f'END of {__file__}')
