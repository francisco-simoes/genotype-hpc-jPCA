chunknumber=134 
chunksize=10000
leftover=$((1343816 - $chunknumber * $chunksize))
echo 'chunknumber: $chunknumber'
echo 'chunksize: $chunksize'
echo 'leftover: $leftover'

minvars=$(for x in $(eval echo {1..$chunknumber}); do echo $(($x * $chunksize + 1)); done)

for minvar in $minvars
do
	echo $minvar
	sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $chunksize
done

#And now the leftover vars:
minvar=$(($chunknumber * $chunksize + 1))
sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $leftover
