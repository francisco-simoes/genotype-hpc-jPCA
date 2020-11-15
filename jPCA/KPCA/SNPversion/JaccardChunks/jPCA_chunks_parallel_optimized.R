args <- commandArgs(trailingOnly = TRUE)
minvar = as.integer(args[1])
chunksize = as.integer(args[2])
maxvar = minvar + chunksize - 1 

gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb`
#if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)} #Divide `var` in chunks.
var=var[minvar:maxvar] # Load the sample genotypes for target variants
GT=rvat::loadGT(gdb, var, SM=SM)  # Kick out everything except the rare variants
GT$flipToMinor()
GT$smFilter(!is.na(GT$SM$IID) & GT$SM$pheno %in% c(0,1))
#GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7) #Rare variants (only).
GT$varFilter(GT$af>0.01 & GT$af>0 & GT$genoVar>0.7) #Common variants (only).
SM <- GT$SM
# Get rid of NAs:
#GT$missingToRef() #NAs turn to zeros.  for (i in 1:now(SM))
GT$GT[is.na(GT$GT)]=0
GT <- GT$GT

different_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m01,m02,m10,m12,    m20,m21
equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m11,m22.

GT0 <- GT==0
GT1 <- GT==1
GT2 <- GT==2

time1 <- Sys.time()
different_positive_count = GT0 %*% t(GT1) + GT0 %*% t(GT2) + GT1 %*% t(GT0) + GT1 %*% t(GT2) + GT2 %*% t(GT0) + GT2 %*% t(GT1)

equal_positive_count =  GT1 %*% t(GT1) + GT2 %*% t(GT2)

time2 <- Sys.time()
print('Computation delta t:')
print(time2-time1)

saveRDS(different_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/mijs/diff_pos_count_%s.rds", minvar))
saveRDS(equal_positive_count,file=sprintf("/hpc/hers_en/fsimoes/jPCA/KPCA/SNPversion/JaccardChunks/mijs/eq_pos_count_%s.rds", minvar))
