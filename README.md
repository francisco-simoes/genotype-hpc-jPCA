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



	


