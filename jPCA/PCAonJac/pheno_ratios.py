'''
Compute the ratios of each pheno on each section of the Histogram.
Assumes that a pheno dictionary pickle file has already been generated.
'''

import pickle
import jPCA_settings

# Import pheno dictionary
with open('/hpc/hers_en/fsimoes/logs/objects/section_phenos_dicts.pkl', 'rb') as file:
    section_phenos = pickle.load(file)

# Print ratios for each pheno, in each section:
for i in range(len(section_phenos)): #Cycle over sections of the histogram.
    print('\n --- Section {} --- '.format(i) )
    section_dict = section_phenos[i]
    section_total = sum(section_dict.values()) #Total number of individuals in section i.
    for key, value in section_dict.items():
        #The ratio answers the question: 
        #what is the representation of the pheno `key` in the section `i`?
        ratio = value / section_total
        print('Ratio of pheno {} in section {}: {}'.format(key, i, ratio))

# Compare ratios between sections:
for key in section_phenos[0].keys(): #All dictionaries have the same keys...
    print('\n --- Pheno <{}> --- '.format(key))
    for i in range(len(section_phenos)): #Cycle over sections of the histogram.
        section_dict = section_phenos[i]
        section_total = sum(section_dict.values()) #Total number of individuals in section i.
        value = section_dict[key]
        ratio = value / section_total
        print('Ratio in section {}: {}'.format(i, ratio))


