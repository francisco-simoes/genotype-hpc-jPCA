args <- commandArgs(trailingOnly = TRUE)
chunknumber = as.integer(args[1])
chunksize = as.integer(args[2])

print('chunknumber:')
print(chunknumber)
print('chunksize:')
print(chunksize)

minvars <- lapply(0:(chunknumber+1), function(x) x*chunksize+1)
#(chunknumber+1) in the first arg to account for the leftover chunk.
print('minvars length:')
print(length(minvars))
print('minvars:')
print(minvars)

##Define SM to get dims.
#gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"
#gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
#SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
#var=scan("VAR_id.txt") 
#GT=rvat::loadGT(gdb, var, SM=SM)  # Kick out everything except the rare variants
#GT$flipToMinor()
#GT$smFilter(!is.na(GT$SM$IID) & GT$SM$pheno %in% c(0,1))
#GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7)
#SM <- GT$SM

#Get dimensions from a sample matrix
eq_pos_count_sample=readRDS("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/eq_pos_count_1.rds")
dims = dim(eq_pos_count_sample)

Different_positive_count=matrix(0,nrow=dims[1],ncol=dims[2]) #Replaces M01,M02,M10,M12,M20,M21
Equal_positive_count=matrix(0,nrow=dims[1],ncol=dims[2]) #Replaces M11,M22.

for (minvar in minvars)
{
	print('Current minvar:')
	print(minvar)

	equal_positive_count = readRDS(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/eq_pos_count_%s.rds", minvar))
	print(typeof(Equal_positive_count))
	print(typeof(equal_positive_count))
	print(dim(Equal_positive_count))
	print(dim(equal_positive_count))
	Equal_positive_count = Equal_positive_count + equal_positive_count

	different_positive_count = readRDS(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/diff_pos_count_%s.rds", minvar))
	Different_positive_count = Different_positive_count + different_positive_count
#	M01=M01+m01
#	M02=M02+m02
#	M10=M10+m10
#	M11=M11+m11
#	M12=M12+m12
#	M20=M20+m20
#	M21=M21+m21
#	M22=M22+m22
}
print('loop end')

#gram=(M11 + M22) / (M01 + M02 + M10 + M11 + M12 + M20 + M21 + M22)
gram <- Equal_positive_count / (Equal_positive_count + Different_positive_count)
write.table(gram,file="jaccard_gram_R.txt",quote=F,sep="\t")
