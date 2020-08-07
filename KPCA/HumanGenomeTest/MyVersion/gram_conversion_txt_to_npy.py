'''
Convert jaccard_gram_R_eur_rare.txt to .npy.
'''
import numpy as np
nvars=500000
GRAM = np.loadtxt('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_eur_rare_with_{}_vars.txt'.format(nvars), skiprows=1)
GRAM = GRAM[:,1:] #First column just has indices.
print('Similarity matrix shape:', GRAM.shape)
print('Saving .npy file...')

np.save('/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_eur_rare_with_{}_vars.txt'.format(nvars),GRAM)
print('done')
