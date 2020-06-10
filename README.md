# Description of the jPCA pipelines

## Pipeline description

All pipelines follow the same format:

[input matrix](e.g. indiv_counts_LOF...txt) > [[Converter to npy]](txt_to_npy...py) > [(rounded) matrix with no NAs](no_NAs...npy) > [[Jaccard matrix generator]](jPCA_jaccard...py) >> [OUTPUT 1: Jaccard heatmap] > [jaccard matrix](jaccard...npy) > [[Histogram generator]] >> [OUTPUT 2: Histogram]

## Rounded vs not rounded and the different pipelines

- The standard pipeline is the one with rounded burden values.
	> The reason for this is that if we use mean-imputed values there will be a lot of individuals with the same nonzero burdens (and so in particular will get high Jaccard similarity values), but this will simply mean that original these individuals had missing values in the same genes. I think this can even be a confounding factor for non-Jaccard methods...

- There are three pipelines so far:
	- One with rounding.
	- One without rounding.
	- One with rounding and extra bins in the histogram.

# Auxiliary modules:

- Settings file: contains the parameters used in the scripts of the pipeline, so that we don't have to chance them separately.
- Functions file: contains the functions we use in the scripts of the pipeline.
- Genotype diagnostics file: prints useful values like percentage of zeros before and after rounding.


# Why do we check the univariate Gaussianity of J(i,j)?

- Every individual's burden can be seen as a random variable equal to any other individual's burden.
- Hence each entry of the similarity matrix (each Jaccard value) can be seen as a random variable coming from the same distribution.
- This means that we can get a visual representation of the distribution by simply using all the Jaccard values, as if they were the same random variable... because they are!
- Multivariate Gaussianity is not necessary, but it is sufficient, for two of the PCA assumptions to be satisfied: linearity and orthogonality of principal components.
- It is important to note that Gaussianity of some variables does not mean that the multivariate distribution is Gaussian! (Did not get the intuition behind this yet). However, if the variables are independent (as in our case) then this is true, *I think*. So it does make sense to look at the Gaussianity of all J(i,j) to conclude that the multivariate distribution for the random vector $(J(i,j))_{i,j}$ is indeed multivariate Gaussian.
- Notice that our problem can reside in the third assumption of PCA (when used for dimensionality reduction): that most of the variance of the data resides in a low dimensional subspace of the sample space. And this actually seems to fail.
