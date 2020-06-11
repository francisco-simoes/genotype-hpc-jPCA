'''
Compute the ratios of each cohort on each section of the Histogram.
Assumes that a cohort dictionary pickle file has already been generated.
'''

import pickle
import jPCA_settings

# Import cohort dictionary
with open('/hpc/hers_en/fsimoes/logs/objects/section_cohorts_dicts.pkl', 'rb') as file:
    section_cohorts = pickle.load(file)

# Print ratios for each cohort, in each section:
for i in range(len(section_cohorts)): #Cycle over sections of the histogram.
    print('\n --- Section {} --- '.format(i) )
    section_dict = section_cohorts[i]
    section_total = sum(section_dict.values()) #Total number of individuals in section i.
    for key, value in section_dict.items():
        #The ratio answers the question: 
        #what is the representation of the cohort `key` in the section `i`?
        ratio = value / section_total
        print('Ratio of cohort {} in section {}: {}'.format(key, i, ratio))

# Compare ratios between sections:
for key in section_cohorts[0].keys(): #All dictionaries have the same keys...
    print('\n --- Cohort <{}> --- '.format(key))
    for i in range(len(section_cohorts)): #Cycle over sections of the histogram.
        section_dict = section_cohorts[i]
        section_total = sum(section_dict.values()) #Total number of individuals in section i.
        value = section_dict[key]
        ratio = value / section_total
        print('Ratio in section {}: {}'.format(i, ratio))


