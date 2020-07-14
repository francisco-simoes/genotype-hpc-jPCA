args <- commandArgs(trailingOnly = TRUE)
minvar = args[1]
chunksize = args[2]
maxvar = minvar + chunksize

gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb`
#if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)} #Divide `var` in chunks.
var=var[minvar:maxvar]
m01=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m02=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m10=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m11=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m12=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m20=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m21=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
m22=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) 
# Load the sample genotypes for target variants
GT=rvat::loadGT(gdb, var[[i]], SM=SM)  # Kick out everything except the rare variants
GT$flipToMinor()
# kick out everything except rare high call rate variants
GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7)
# Get rid of NAs:
GT$missingToRef() #NAs turn to zeros.  for (i in 1:now(SM))
for (i in 1:nrow(SM)) #Cycle over individuals)
{
	for(j in 1:nrow(SM))
	{
	m01[i,j]=sum(GT$GT[i,] == 0 & GT$GT[j,] == 1)
	m02[i,j]=sum(GT$GT[i,] == 0 & GT$GT[j,] == 2)
	m10[i,j]=sum(GT$GT[i,] == 1 & GT$GT[j,] == 0)
	m11[i,j]=sum(GT$GT[i,] == 1 & GT$GT[j,] == 1)
	m12[i,j]=sum(GT$GT[i,] == 1 & GT$GT[j,] == 2)
	m20[i,j]=sum(GT$GT[i,] == 2 & GT$GT[j,] == 0)
	m21[i,j]=sum(GT$GT[i,] == 2 & GT$GT[j,] == 1)
	m22[i,j]=sum(GT$GT[i,] == 2 & GT$GT[j,] == 2)
	}
}

save(m01,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m01_%s:%s.rda", minvar, maxvar))
save(m02,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m02_%s:%s.rda", minvar, maxvar))
save(m10,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m10_%s:%s.rda", minvar, maxvar))
save(m11,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m11_%s:%s.rda", minvar, maxvar))
save(m12,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m12_%s:%s.rda", minvar, maxvar))
save(m20,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m20_%s:%s.rda", minvar, maxvar))
save(m21,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m21_%s:%s.rda", minvar, maxvar))
save(m22,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/m22_%s:%s.rda", minvar, maxvar))
