minvars=
chunksize=
for minvar in minvars
do
	/hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel.R $minvar $chunksize
done
