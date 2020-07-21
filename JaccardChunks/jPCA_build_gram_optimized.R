args <- commandArgs(trailingOnly = TRUE)
chunknumber = as.integer(args[1])
chunksize = as.integer(args[2])

minvars <- lapply(0:chunknumber-1, function(x) x*chunksize+1)
print('minvars length:')
print(length(minvars))

gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")

Different_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces M01,M02,M10,M12,M20,M21
Equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces M11,M22.

for (minvar in minvars)
{
	print('Current minvar:')
	print(minvar)
	different_positive_count = load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/diff_pos_count_%s.rda", minvar))
	equal_positive_count = load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/eq_pos_count_%s.rda", minvar))

	Equal_positive_count = Equal_positive_count + equal_positive_count
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

#gram=(M11 + M22) / (M01 + M02 + M10 + M11 + M12 + M20 + M21 + M22)
gram <- Equal_positive_count / (Equal_positive_count + Different_positive_count)
write.table(gram,file="jaccard_gram_R.txt",quote=F,sep="\t")
