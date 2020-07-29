'''
Creates heatmap of the gram matrix.
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#plt.ion() # script will continue running after show().
plt.style.use('seaborn-white')

GRAM = np.load('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.npy')
print('Similarity matrix shape:', GRAM.shape)

# Heatmap with gram matrix:
plt.figure()
plt.imshow(GRAM, cmap='hot')
plt.colorbar()
plt.title('Similarity matrix colormap; SNP version')
plt.savefig('/hpc/hers_en/fsimoes/logs/images/Gram_heatmap_SNP-version.png')
