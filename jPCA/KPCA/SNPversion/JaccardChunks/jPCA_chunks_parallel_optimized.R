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
print('before var scan')
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb`
#if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)} #Divide `var` in chunks.
var=var[minvar:maxvar] # Load the sample genotypes for target variants
print('var length:')
print(length(var))
print('before GT rvat')
GT=rvat::loadGT(gdb, var, SM=SM)  # Kick out everything except the rare variants
print('before flipToMinor')
GT$flipToMinor()
# kick out everything except rare high call rate variants
print('before filter')
GT$smFilter(!is.na(GT$SM$IID) & GT$SM$pheno %in% c(0,1))
#GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7) #Rare variants.
GT$varFilter(GT$af>0.01 & GT$af>0 & GT$genoVar>0.7) #Common variants.
SM <- GT$SM
# Get rid of NAs:
print('before NA removal')
#GT$missingToRef() #NAs turn to zeros.  for (i in 1:now(SM))
GT$GT[is.na(GT$GT)]=0
GT <- GT$GT

print('before defining different_positive_count')
different_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m01,m02,m10,m12,    m20,m21
print('before defining equal_positive_count')
equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m11,m22.

print('before defining GT0,1,2')
GT0 <- GT==0
GT1 <- GT==1
GT2 <- GT==2

time1 <- Sys.time()
print('before diff count computation')
different_positive_count = GT0 %*% t(GT1) + GT0 %*% t(GT2) + GT1 %*% t(GT0) + GT1 %*% t(GT2) + GT2 %*% t(GT0) + GT2 %*% t(GT1)

print('before equal count computation')
equal_positive_count =  GT1 %*% t(GT1) + GT2 %*% t(GT2)

time2 <- Sys.time()
print('Computation delta t:')
print(time2-time1)

saveRDS(different_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/mijs/diff_pos_count_%s.rds", minvar))
saveRDS(equal_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/mijs/eq_pos_count_%s.rds", minvar))
