# Pipeline for getting the Jaccard matrix from data chunks

- `parallelizing_loop_optimized.sh` runs many `jPCA_chunks_parallel_optimized.R`, each for a different chunk of the variants, until all variants in `VAR_id(_PCA).txt` are covered.
	* Each `jPCA_chunks_parallel_optimized.R` creates a `diff_pos_count` and a `eq_pos_count` file. Hence `parallelizing_loop_optimized.sh` creates the `diff_pos_count` and `eq_pos_count` files, storing them in the directory `mijs`. These are matrices whose entries are the number of entries where the genotype values of pairs of individuals differ/coincide *and* at least one of the genotype values is positive.
- `build_gram_optimized.sh` runs `jPCA_build_gram_optimized.R` with the appropriate arguments.
	* `jPCA_build_gram_optimized.R` builds the gram matrix from the `mij`.

#To run all this with a single shell script, one must compute chunknumber and define chunksize (as 10000 probably).
