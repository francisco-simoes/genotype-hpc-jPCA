# The Kernel PCA scripts

## Gene-burden data
The initial focus of the project was on gene-burden data.
The scripts in the `GeneBurdenVersion` directory  deal with said data.
More concretely:
1. All the scripts in this directory use the Jaccard matrix computed in `PCAonJac/jPCA_jaccard_matrix.py` and the settings (like the number `N` of samples to use) from `jPCA_settings.py`. `N=30820` corresponds to the entire dataset.
2. `GeneBurdenVersion/kPCA_on_sim_matrix_NO_SCALING.py` gets the PC scores using sklearn's KernelPCA and the precomputed Jaccard matrix as the kernel.
3. `GeneBurdenVersion/kPCA_glm_pheno_statsmodels.py` runs glm with binomial family (basically logistic regression for binomial counts) on the PC scores, printing useful values like p-values and coefficients.
4. `GeneBurdenVersion/kPCA_labelling_(something).py` plot the first two PCs and labels the data with `something` from the pheno matrix.
5. `GeneBurdenVersion/kPCA_pc_correlation.py` creates a heatmap showing how our PCs correlate with the PCs obtained performing standard PCA on genotype data.

## SNP-burden (genotype) data
The Jaccard matrix constructed by `PCAonJac/jPCA_jaccard_matrix.py` does not apply anymore, so we need to construct anothe Jaccard matrix.
This data was too large to construct the Jaccard matrix directly on the hpc.
So we have parallelize the constructor by dividing the data in chunks (I used 135 chunks with 10000 variants each) and putting everything back together afterwards. 
The scripts to construct the Jaccard matrix are in `SNPversion/JaccardChunks/` and a description on how to use them is given in `SNPversion/JaccardChunks/README.md`.
The scripts in `SNPversion/` are similar in name and function to the ones in `GeneBurdenVersion/`, described above.

## Testing my kernel PCA algorithm in the Human Genome Project data
To make sure that my Jaccard KPCA algorithm works, I ran it on a chunk of the Human Genome Project data and compared the resulting plot with the plot obtained by using the `jacpop` function from Dmitry's paper on jPCA. 
The files I used are in `HumanGenomeTest/`.
_Note_: Why not using `jacpop` for our data as well, then? Because the `jacpop` function needed to be used in the entire data, and our dataset was to big for that - we needed to parallelize it. 
Also, I prefer to use Python over R, and there was no alternative to `jacpop` written in Python until now.
Finally, by contructing our own algorithms we can extract any information we want from the data.

## Loose files
1. `glm_pheno_OG_pcs.py` runs glm on the PC scores from standard PCA on the genotype data (which had been computed beforehand by a colleague). We can then compare these results with ours.
2. `test_kpca_sklearn.py` tests KernelPCA on a typical example.
3. `test_jaccard_kpca_sklearn.py` adapts KernelPCA to a Jaccard Kernel on the same example as before.
