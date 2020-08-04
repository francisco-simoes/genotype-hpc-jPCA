# A function that rounds up after division of num/denom:
function round_up_division {
	let local num=$1
	let local denom=$2
	echo $(( ($num + $denom - 1)/$denom  ))
}

# Necessary variables
#totalvars=$(wc -l < /hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/VAR_id.txt)
totalvars=$(wc -l < /hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/VAR_id_PCA.txt)
chunksize=10000 #Chosen from experience.
chunknumber=$(round_up_division $totalvars $chunksize ) 
if [ $(($totalvars % $chunksize)) -ne 0 ] #when last chunk has less vars.
then
	#Number of vars in last chunk:
	leftover=$(($totalvars - ($chunknumber-1) * $chunksize)) 
else
	leftover=0
fi

echo 'totalvars' $chunknumtotalvars
echo 'chunksize:' $chunksize
echo 'chunknumber:' $chunknumber
echo 'leftover:' $leftover

# Get counts with parallel scripts.
echo 'Parallelizing $chunknumber scripts to get counts in mijs/ directory...'
bash /hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/parallelizing_loop_optimized.sh $totalvars $chunksize $chunknumber $leftover

# Build Gram matrix
echo 'Building Gram matrix!'
bash /hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/build_gram_optimized.sh $totalvars $chunksize $chunknumber $leftover

# Build Gram matrix
echo 'Building Gram matrix!'
bash /hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/build_gram_optimized.sh $totalvars $chunksize $chunknumber $leftover
