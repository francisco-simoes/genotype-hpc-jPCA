'''
jPCA as KPCA with a Jaccard kernel on the typical KPCA toy model with circles, using KernelPCA from sklearn.
Naturally the result will be bad (most pairs of points have Jaccard scores of zero), but I want to make sure the code runs.
'''
import sys
sys.path.append('/hpc/hers_en/fsimoes/jPCA')

import numpy as np
import matplotlib.pyplot as plt

from jPCA_functions import generalized_jaccard_score
from sklearn.decomposition import PCA, KernelPCA
from sklearn.datasets import make_circles

np.random.seed(0)

X, y = make_circles(n_samples=400, factor=.3, noise=.05)

##kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)
#def kernel_rbf(x, y, gamma):
#    return np.exp(-gamma * np.dot(x - y, x - y))
#kpca = KernelPCA(kernel='precomputed', kernel_params={'gamma': 10}) #The parameters of a precomputed kernel must be in a dictionary fed to `kernel_params`.

# Build the Gram matrix (the similarity matrix):
kpca = KernelPCA(kernel='precomputed')

def build_gram(X, kernel_func, func_params : 'dict' = {}):
    G = np.zeros((X.shape[0], X.shape[0])) #X.shape[0]=number of samples
    for i in range(G.shape[0]):
        for j in range(G.shape[1]):
            x_i = X[i, :]
            y_j = X[j, :]
            G[i,j] = kernel_func(x_i, y_j, **func_params)
    return G

gram = build_gram(X, generalized_jaccard_score)
print('Gram matrix shape:', gram.shape)

X_kpca = kpca.fit_transform(gram) 
#X_back = kpca.inverse_transform(X_kpca)
pca = PCA()
X_pca = pca.fit_transform(X)

# Plot results
plt.figure()
plt.subplot(2, 2, 1, aspect='equal')
plt.title("Original space")
reds = y == 0
blues = y == 1

plt.scatter(X[reds, 0], X[reds, 1], c="red",
            s=20, edgecolor='k')
plt.scatter(X[blues, 0], X[blues, 1], c="blue",
            s=20, edgecolor='k')
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")

plt.subplot(2, 2, 2, aspect='equal')
plt.scatter(X_pca[reds, 0], X_pca[reds, 1], c="red",
            s=20, edgecolor='k')
plt.scatter(X_pca[blues, 0], X_pca[blues, 1], c="blue",
            s=20, edgecolor='k')
plt.title("Projection by PCA")
plt.xlabel("1st principal component")
plt.ylabel("2nd component")

plt.subplot(2, 2, 3, aspect='equal')
plt.scatter(X_kpca[reds, 0], X_kpca[reds, 1], c="red",
            s=20, edgecolor='k')
plt.scatter(X_kpca[blues, 0], X_kpca[blues, 1], c="blue",
            s=20, edgecolor='k')
plt.title("Projection by KPCA")
plt.xlabel(r"1st principal component in space induced by $\phi$")
plt.ylabel("2nd component")

plt.tight_layout()
plt.show()
