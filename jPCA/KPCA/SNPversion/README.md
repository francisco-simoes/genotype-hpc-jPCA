## Order in which to run the code:

(Assuming the Jaccard/Gram matrix has been constructed already (using the files in `JaccardChunks/`))
1. Convert the Gram matrix to the `.npy` format using `jaccard_gram_conversion_txt_to_npy.py`. May run `gram_heatmap.py` afterwards to obtain a graphical representation of th e matrix.
2. Run Kernel PCA on the Gram matrix with `kPCA_on_sim_matrix_NO_SCALING.py`. The output is:
	* A matrix with PC scores, with name `X_kpca_...`.
	* A plot of the data using the first two PC scores, named `kPCA_PCs_...`.
3. Run any of the other scripts to obtain the respective plots/prints (data labelled by cohort (`kPCA_labelling_cohort_no_nas.py`); glm regression using pheno as response (`kPCA_glm_pheno_statsmodels.py`); etc.
