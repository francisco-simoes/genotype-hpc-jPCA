echo 'START of' $0
# A function that rounds up after division of num/denom:
function round_up_division {
	let local num=$1
	let local denom=$2
	echo $(( ($num + $denom - 1)/$denom  ))
}

# Necessary variables
totalvars=$(wc -l < /hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/variants_shuffled.txt)
chunksize=10000 #Chosen from experience.
chunknumber=$(round_up_division $totalvars $chunksize ) 
if [ $(($totalvars % $chunksize)) -ne 0 ] #when last chunk has less vars.
then
	#Number of vars in last chunk:
	leftover=$(($totalvars - ($chunknumber-1) * $chunksize)) 
else
	leftover=0
fi

echo 'totalvars:' $totalvars
echo 'chunksize:' $chunksize
echo 'chunknumber:' $chunknumber
echo 'leftover:' $leftover

# Get counts with parallel scripts.
echo 'Submitting job to Parallelize' $chunknumber 'scripts in order to get counts in mijs/ directory...'
sbatch --job-name=counts_sh execute_10G.sh bash /hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/MyVersion/ParallelizedVersion/JaccardChunks/parallelizing_loop_optimized.sh $totalvars $chunksize $chunknumber $leftover

sleep 10 #Give it some time for the jaccard_chunks jobs to be submitted.
# Build Gram matrix - after the mijs have been computed.
echo 'Submitting job to build Gram matrix!'
sbatch --dependency=singleton --job-name=jaccard_chunks execute_10G.sh bash /hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/MyVersion/ParallelizedVersion/JaccardChunks/build_gram_optimized.sh $totalvars $chunksize $chunknumber $leftover

echo 'END of' $0
