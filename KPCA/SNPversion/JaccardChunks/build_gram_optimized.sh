echo 'START of' $0
totalvars=$1
chunksize=$2
chunknumber=$3
leftover=$4

#echo 'totalvars' $chunknumtotalvars
echo 'chunksize:' $chunksize
echo 'chunknumber:' $chunknumber
#echo 'leftover:' $leftover

sbatch --job-name=gram /hpc/hers_en/fsimoes/execute_80G.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_build_gram_optimized.R $chunknumber $chunksize

echo 'Gram matrix built.'
echo 'END of' $0
