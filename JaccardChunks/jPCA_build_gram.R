args <- commandArgs(trailingOnly = TRUE)
chunknumber = args[1]
chunksize = args[2]

minvars <- #[] ???


gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")

M01=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M02=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M10=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M11=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M12=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M20=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M21=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
M22=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
for minvar in minvars
{
	maxvar = minvar+chunksize
	m01=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m01_%s:%s.rda", minvar, maxvar))
	m02=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m02_%s:%s.rda", minvar, maxvar))
	m10=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m10_%s:%s.rda", minvar, maxvar))
	m11=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m11_%s:%s.rda", minvar, maxvar))
	m12=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m12_%s:%s.rda", minvar, maxvar))
	m20=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m20_%s:%s.rda", minvar, maxvar))
	m21=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m21_%s:%s.rda", minvar, maxvar))
	m22=load(sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m22_%s:%s.rda", minvar, maxvar))

	M01=M01+m01
	M02=M02+m02
	M10=M10+m10
	M11=M11+m11
	M12=M12+m12
	M20=M20+m20
	M21=M21+m21
	M22=M22+m22
}

gram=(M11 + M22) / (M01 + M02 + M10 + M11 + M12 + M20 + M21 + M22)
write.table(gram,file="jaccard_gram_R.txt",quote=F,sep="\t")
