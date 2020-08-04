# echo 'Generating rounded matrix...'
# python3 /hpc/hers_en/fsimoes/jPCA/txt_to_npy_matrix_conversion.py

echo 'Generating Jaccard similarity matrix and heatmap...'
python3 /hpc/hers_en/fsimoes/jPCA/jPCA_jaccard_matrix.py

echo 'Generating Jaccard histogram...'
python3 /hpc/hers_en/fsimoes/jPCA/jPCA_hist.py
