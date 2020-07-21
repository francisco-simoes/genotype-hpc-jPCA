args <- commandArgs(trailingOnly = TRUE)
minvar = as.integer(args[1])
chunksize = as.integer(args[2])
print(minvar)
print(chunksize)
maxvar = minvar + chunksize - 1

gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
print('before SM')
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
print('after SM')
print('before var scan')
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb`
print('after var scan')
#if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)} #Divide `var` in chunks.
var=var[minvar:maxvar]
print('before different_positive_count')
different_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m01,m02,m10,m12,m20,m21
print('before equal_positive_count')
equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m11,m22.
# Load the sample genotypes for target variants
print('var length:')
print(length(var))
print('before GT rvat')
GT=rvat::loadGT(gdb, var, SM=SM)  # Kick out everything except the rare variants
print('before flipToMinor')
GT$flipToMinor()
# kick out everything except rare high call rate variants
print('before filter')
GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7)
# Get rid of NAs:
print('before NA removal')
#GT$missingToRef() #NAs turn to zeros.  for (i in 1:now(SM))
GT$GT[is.na(GT$GT)]=0
print('begin loop')
for (i in 1:nrow(SM)) #Cycle over individuals)
{
	print(sprintf('i: %s of %s', i, nrow(SM)))
	for(j in 1:nrow(SM))
	{
		different_positive_count[i,j]= (j>=i) * ( sum(GT$GT[i,] == 0 & GT$GT[j,] == 1) +
		sum(GT$GT[i,] == 0 & GT$GT[j,] == 2) +
		sum(GT$GT[i,] == 1 & GT$GT[j,] == 0) +
		sum(GT$GT[i,] == 1 & GT$GT[j,] == 2) +
		sum(GT$GT[i,] == 2 & GT$GT[j,] == 0) +
		sum(GT$GT[i,] == 2 & GT$GT[j,] == 1) ) + (j<i) * different_positive_count[j,i]
		equal_positive_count[i,j]= (j>=i) * ( sum(GT$GT[i,] == 1 & GT$GT[j,] == 1) +
		sum(GT$GT[i,] == 2 & GT$GT[j,] == 2) ) + (j<i) * equal_positive_count[j,i]
	}
}
print('end loop')

save(different_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/diff_pos_count_%s:%s.rda", minvar, maxvar))
save(equal_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/eq_pos_count_%s:%s.rda", minvar, maxvar))
