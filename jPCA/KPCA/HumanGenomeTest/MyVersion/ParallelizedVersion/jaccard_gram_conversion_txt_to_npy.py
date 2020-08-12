'''
Convert jaccard_gram_R.txt to .npy.
'''
print(f'START of {__file__}')
import numpy as np
#GRAM = np.loadtxt('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.txt', skiprows=1)
#GRAM = np.loadtxt('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_common.txt', skiprows=1)
GRAM = np.loadtxt('/hpc/hers_en/fsimoes/logs/objects/HumanGenomeTest/MyVersion/ParallelizedVersion/jaccard_gram.txt', skiprows=1)
GRAM = GRAM[:,1:] #First column just has indices.
print('Similarity matrix shape:', GRAM.shape)
print('Saving .npy file...')

#np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.npy',GRAM)
#np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_common.npy',GRAM)
np.save('/hpc/hers_en/fsimoes/logs/objects/HumanGenomeTest/MyVersion/ParallelizedVersion/jaccard_gram.npy',GRAM)
print(f'END of {__file__}')
