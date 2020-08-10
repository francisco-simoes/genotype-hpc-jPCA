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
df_old = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
#df_old = df_old.iloc[:N]
#print(df)
#print(df.columns)
print('non-NAs in cohort:', df_old['cohort'].count())
cohorts = df_old['cohort'].unique()
number_of_cohorts=len(cohorts)
#print('\n\nScores (head):\n{}'.format(scores.head()))
print('cohort types:', df_old['cohort'].unique(), '\nNumber of types:', number_of_cohorts)

# Drop nan's
df = df_old.copy(deep=True)
df = df[df['cohort'].notna()]
print('NAs after drop:', len(df['cohort']) - df['cohort'].count())
cohorts = df['cohort'].unique()
number_of_cohorts=len(cohorts)
#print('\n\nScores (head):\n{}'.format(scores.head()))
print('cohort types:', df['cohort'].unique(), '\nNumber of types:', number_of_cohorts)

# Load the PC scores and create scores Dataframe.
#scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca.npy')
#scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common.npy')
scores_matrix = np.load('/hpc/hers_en/fsimoes/logs/objects/SNPversion/kPCA_X_kpca_common_alternative_VAR.npy')
#(One PC for each column).

# Plot with colored classes
#Must drop datapoints corresponding to the nans!
x = scores_matrix[:,0][df_old['cohort'].notna().to_numpy()]
y = scores_matrix[:,1][df_old['cohort'].notna().to_numpy()]
labels = pd.factorize(df['cohort'])[0] #Turn classes numeric.
#Need {number_of_cohorts<=15} colors.
colors_max_case = ['orange','yellow','green', 'blue', 'red', 'violet', 'cyan', 'gold', 'lawngreen', 'sienna', 'lightcoral', 'darkblue', 'saddlebrown', 'grey', 'magenta']
colors = colors_max_case[:number_of_cohorts]

fig = plt.figure(figsize=(8,8))
plt.scatter(x, y, c=labels, cmap=matplotlib.colors.ListedColormap(colors))
cb = plt.colorbar()
print(df_old['cohort'].notna())
loc = np.arange(0,max(labels),max(labels)/float(len(colors)))
cb.set_ticks(loc)
cb.set_ticklabels(cohorts)
plt.title('First two PCs for SNP burdens with cohort labels; alternative vars.')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.savefig('/hpc/hers_en/fsimoes/logs/images/kPCA_cohort_NO_nas_colorized_SNP_common_alternative_VAR.png')
#plt.show()

print(f'END of {__file__}')
