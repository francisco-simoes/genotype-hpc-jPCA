echo 'Building gram matrix!'
#chunknumber=134 
chunknumber=2
#chunksize=10000
chunksize=10
#totalvars=1343816
totalvars=23
leftover=$(($totalvars - $chunknumber * $chunksize))
echo 'chunknumber:' $chunknumber
echo 'chunksize:' $chunksize

sbatch --job-name=gram /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_build_gram_optimized.R $chunknumber $chunksize
