import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import jPCA_settings
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Load necessary settings
N = jPCA_settings.N

# Get labels' dataframe
df = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
df = df.iloc[:N]
#print(df)
#print(df.columns)
print('non-NAs in SequencingCentre:', df['SequencingCentre'].count())
centres = df['SequencingCentre'].unique()
number_of_centres=len(centres)
print('Centre types:', centres, '\nNumber of types:', number_of_centres)

# Load the PC scores and create scores Dataframe.
scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/kPCA_X_kpca_N={}.npy'.format(N))
#(One PC for each column).

# Plot with colored classes
x = scores_matrix[:,0]
y = scores_matrix[:,1]
labels = pd.factorize(df['SequencingCentre'])[0] + 1 #Turn classes numeric.
#(+1 is important so that Nans are read as 0 instead of -1)
#Need {number_of_centres=8} colors.
colors_max_case = ['black','orange','yellow','green', 'blue', 'red', 'violet', 'cyan']
colors = colors_max_case[:number_of_centres]

fig = plt.figure(figsize=(8,8))
plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
cb = plt.colorbar()
loc = np.arange(0,max(labels),max(labels)/float(len(colors)))
cb.set_ticks(loc)
cb.set_ticklabels(centres)
plt.title('First two PCs for N={}'.format(N))
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.savefig(('/hpc/hers_en/fsimoes/logs/images/kPCA_centres_colorized_N={}'.format(N)))
#plt.show()
