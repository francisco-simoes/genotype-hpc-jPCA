'''
Run statsmodels' logistic regression on kPCA scores with the phenotype as the response, and prints main metrics and Z-scores, p-values.
'''

import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import jPCA_settings
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# Load necessary settings
N = jPCA_settings.N
n_pcs_to_use = jPCA_settings.n_pcs_to_use

# Get labels' dataframe
df = pd.read_csv('/hpc/hers_en/fsimoes/wxs/Relevant/mine_wxs_180919.postPCA.pheno', sep='\t')
df = df.iloc[:N]
#print(df)
print(df.columns)
phenos = df['pheno'].unique()
number_of_phenos = len(phenos)
print('Phenos:', df['pheno'].unique())

# Load the PC scores and create scores Dataframe.
X_kpca = np.load('/hpc/hers_en/fsimoes/logs/objects/kPCA_X_kpca_N={}.npy'.format(N)) #This is the scores matris!
X_kpca = X_kpca[:, :n_pcs_to_use]
print('Scores matrix shape: ', X_kpca.shape)
#(One PC for each column).

# Get responses
labels = df['pheno'].factorize()[0] #1D array. One entry for each sample.

# Create train-test sets
X_train, X_test, y_train, y_test = train_test_split(X_kpca, labels, test_size=0.20, random_state=42)
print('Training set size: {}\nTest set size: {}'.format(len(y_train), len(y_test)))

# Fit binomial glm with statsmodels
print('------------statsmodels binomial glm------------------')
X_train = sm.add_constant(X_train) #statsmodels' assumes column of ones for intercept.
X_test = sm.add_constant(X_test) #statsmodels' assumes column of ones for intercept.
model_sm = sm.GLM(y_train, X_train, family=sm.families.Binomial())

fitted_sm = model_sm.fit() #Doesn't have saga. bfgs gives noninvert Hessian error.
print(fitted_sm.summary2().tables[1])
print(fitted_sm.summary())


# Evaluate the model 
print('\n--- metrics ---')
y_train_pred = np.rint(fitted_sm.predict(X_train)) # statsmodels does not make the prediction, just givest the probs.
print(y_train)
recall_train = recall_score(y_train, y_train_pred)
precision_train = precision_score(y_train, y_train_pred)
accuracy_train = accuracy_score(y_train, y_train_pred)
f1_train = f1_score(y_train, y_train_pred)

y_test_pred = np.rint(fitted_sm.predict(X_test))
recall_test = recall_score(y_test, y_test_pred)
precision_test = precision_score(y_test, y_test_pred)
accuracy_test = accuracy_score(y_test, y_test_pred)
f1_test = f1_score(y_test, y_test_pred)

metrics_dict = {'Recall':[recall_train, recall_test], 'Precision':[precision_train, precision_test], 'Accuracy':[accuracy_train, accuracy_test], 'F1-score':[f1_train, f1_test]}
metrics_df = pd.DataFrame(metrics_dict, index=['train', 'test'])

print(metrics_df)
