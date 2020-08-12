'''
Creates heatmap of the gram matrix.
(May run interactively if no X display is available).
'''
print(f'START of {__file__}')

import numpy as np
import matplotlib as mpl
mpl.use('Agg') #Won't need X display.
import matplotlib.pyplot as plt

#plt.ion() # script will continue running after show().
plt.style.use('seaborn-white')

#GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.npy')
#GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_common.npy')
GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/HumanGenomeTest/MyVersion/ParallelizedVersion/jaccard_gram.npy')
print('Similarity matrix shape:', GRAM.shape)

# Heatmap with gram matrix:
plt.figure()
plt.imshow(GRAM, cmap='hot')
plt.colorbar()
plt.title('Similarity matrix colormap; parallelized human genome version')
#plt.savefig('/hpc/hers_en/fsimoes/logs/images/Gram_heatmap_common_SNP-version.png')
#plt.savefig('/hpc/hers_en/fsimoes/logs/images/Gram_heatmap_SNP-version_common.png')
plt.savefig('/hpc/hers_en/fsimoes/logs/images/Gram_heatmap_parallelized_human_genome.png')

print(f'END of {__file__}')
