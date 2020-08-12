args <- commandArgs(trailingOnly = TRUE)
chunknumber = as.integer(args[1])
chunksize = as.integer(args[2])

print('Start of the Gram builder (R)')

print('chunknumber:')
print(chunknumber)
print('chunksize:')
print(chunksize)

minvars <- lapply(0:chunknumber, function(x) x*chunksize+1)
#(chunknumber+1) in the first arg to account for the leftover chunk.
print('minvars length:')
print(length(minvars))
print('minvars:')
print(minvars)

#Get dimensions from a sample matrix
eq_pos_count_sample=readRDS("/hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/MyVersion/ParallelizedVersion/JaccardChunks/mijs/eq_pos_count_1.rds")
dims = dim(eq_pos_count_sample)

Different_positive_count=matrix(0,nrow=dims[1],ncol=dims[2]) #Replaces M01,M02,M10,M12,M20,M21
Equal_positive_count=matrix(0,nrow=dims[1],ncol=dims[2]) #Replaces M11,M22.

for (minvar in minvars)
{
	print('Current minvar:')
	print(minvar)

	equal_positive_count = readRDS(sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/MyVersion/ParallelizedVersion/JaccardChunks/mijs/eq_pos_count_%s.rds", minvar))
	Equal_positive_count = Equal_positive_count + equal_positive_count
	rm(equal_positive_count); gc() #Clean up to save up RAM

	different_positive_count = readRDS(sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/HumanGenomeTest/MyVersion/ParallelizedVersion/JaccardChunks/mijs/diff_pos_count_%s.rds", minvar))
	Different_positive_count = Different_positive_count + different_positive_count
	rm(different_positive_count); gc() #Clean up to save up RAM
}
print('loop end')

gram <- Equal_positive_count / (Equal_positive_count + Different_positive_count)

#gram has NAs wherever the total positive count is zero -> set those to zero:
print("number of nas:")
print(sum(is.na(gram)))
print("number of non-nas:")
print(sum(!is.na(gram)))
gram[is.na(gram)]=0
print('nas have been cleaned. Writing file...')

write.table(gram,file="/hpc/hers_en/fsimoes/logs/objects/HumanGenomeTest/MyVersion/ParallelizedVersion/jaccard_gram_R_alternative_VAR.txt",quote=F,sep="\t")
#write.table(gram,file="/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_common.txt",quote=F,sep="\t")
#write.table(gram,file="/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R.txt",quote=F,sep="\t")
print('END of the Gram builder (R)')
