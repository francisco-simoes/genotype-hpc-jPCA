chunknumber=3
chunksize=10
minvars=$(for x in $(eval echo {1..$chunknumber}); do echo $(($x * $chunksize + 1)); done)
for minvar in $minvars
do
	echo $minvar
	sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel.R $minvar $chunksize
done
