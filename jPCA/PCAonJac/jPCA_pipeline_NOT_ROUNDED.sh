echo 'Generating NOT rounded matrix...'
python3 /hpc/hers_en/fsimoes/jPCA/txt_to_npy_matrix_conversion_NOT_ROUNDED.py

echo 'Generating Jaccard similarity matrix and heatmap...'
python3 /hpc/hers_en/fsimoes/jPCA/jPCA_jaccard_matrix_NOT_ROUNDED.py

echo 'Generating Jaccard histogram...'
python3 /hpc/hers_en/fsimoes/jPCA/jPCA_hist_NOT_ROUNDED.py
