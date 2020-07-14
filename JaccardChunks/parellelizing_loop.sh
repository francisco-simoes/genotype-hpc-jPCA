chunknumber=
chunksize=10000
minvars=$(for {1..chunknumber}; do echo $(($x*$chunksize + 1)); done)
for minvar in minvars
do
	/hpc/hers_en/shared/wxs/miniconda3/bin/Rscript /hpc/hers_en/fsimoes/jPCA/JaccardChunks/jPCA_chunks_parallel.R $minvar $chunksize
done
