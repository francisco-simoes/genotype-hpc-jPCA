'''
Convert jaccard_gram_R.txt to .npy.
'''
import numpy as np
GRAM = np.loadtxt('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.txt', skiprows=1)
GRAM = GRAM[:,1:] #First column just has indices.
print('Similarity matrix shape:', GRAM.shape)
print('Saving .npy file...')

np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.npy',GRAM)
print('done')
