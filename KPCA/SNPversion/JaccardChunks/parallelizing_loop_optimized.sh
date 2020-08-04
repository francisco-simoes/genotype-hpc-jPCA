echo 'START of' $0
totalvars=$1
chunksize=$2
chunknumber=$3
leftover=$4

echo 'totalvars' $chunknumtotalvars
echo 'chunksize:' $chunksize
echo 'chunknumber:' $chunknumber
echo 'leftover:' $leftover

# Get counts for all chunks except the last one:
## Get the minvars: var numbers where each chunk starts.
chunkfinal=$(($chunknumber-1-1)) #To account for 0 in {0..$chunkfinal} and exclude the last chunk.
minvars=$(for x in $(eval echo {0..$chunkfinal}); do echo $(($x * $chunksize + 1)); done)

## Run the scripts in parallel:
for minvar in $minvars
do
	echo 'Current minvar:' $minvar
	sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $chunksize
done

# And now for the leftover vars (the last chunk):
minvar=$(($chunknumber * $chunksize + 1))
echo 'Last minvar:' $minvar
sbatch --job-name=jaccard_chunks /hpc/hers_en/fsimoes/execute.sh /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel_optimized.R $minvar $leftover

echo 'Counting completed.'
echo 'END of' $0
