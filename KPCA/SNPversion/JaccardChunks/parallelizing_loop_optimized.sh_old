chunknumber=134 
chunksize=10000
totalvars=1343816
#chunknumber=2
#chunksize=10
#totalvars=23
leftover=$(($totalvars - $chunknumber * $chunksize))
echo 'chunknumber:' $chunknumber
echo 'chunksize:' $chunksize
echo 'leftover:' $leftover

chunkfinal=$(($chunknumber-1))
minvars=$(for x in $(eval echo {0..$chunkfinal}); do echo $(($x * $chunksize + 1)); done)

for minvar in $minvars
do
	echo 'minvar:' $minvar
	sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $chunksize
done

#And now the leftover vars:
minvar=$(($chunknumber * $chunksize + 1))
echo $minvar
sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $leftover
