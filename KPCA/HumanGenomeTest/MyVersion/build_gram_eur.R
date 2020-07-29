# Note the VAR_id must be loaded from this file (these have been "LD pruned" as per Dmitry et al)
var=scan("/hpc/hers_en/kkenna/rvat_tutorial/variants.txt")
#var=var[minvar:maxvar]
gdb="/hpc/hers_en/kkenna/rvat_tutorial/phase3_shapeit2_mvncall_integrated_v5a.20130502.gdb"
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
# Note this time the sample data comes from table "EUR" not "postPCA"
SM <- RSQLite::dbGetQuery(gdb, "select * from EUR")
GT=rvat::loadGT(gdb, VAR_id=var, SM=SM)
GT$flipToMinor()
GT$smFilter(!is.na(GT$SM$IID) & GT$SM$pheno %in% c(0,1))
# remove common variants (af>0.01) and singletons (af=1/(503*2)=0.0009940358)
GT$varFilter(GT$af<=0.01 & GT$af>0.0009940358)
#GT$varFilter(GT$af>0.01 & GT$af>0.0009940358) #remove rare vars and singletons.
GT <- GT$GT

# Get positive counts (different and equal)
print('before defining different_positive_count')
Different_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m01,m02,m10,m12,m20,m21
print('before defining equal_positive_count')
Equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces m11,m22.

print('before defining GT0,1,2')
GT0 <- GT==0
GT1 <- GT==1
GT2 <- GT==2

time1 <- Sys.time()
print('before diff count computation')
Different_positive_count = GT0 %*% t(GT1) + GT0 %*% t(GT2) + GT1 %*% t(GT0) + GT1 %*% t(GT2) + GT2 %*% t(GT0) + GT2 %*% t(GT1)

print('before equal count computation')
Equal_positive_count =  GT1 %*% t(GT1) + GT2 %*% t(GT2)

time2 <- Sys.time()
print('Computation delta t:')
print(time2-time1)

# Building gram
gram <- Equal_positive_count / (Equal_positive_count + Different_positive_count)

#gram has NAs wherever the total positive count is zero -> set those to zero:
print("number of nas:")
print(sum(is.na(gram)))
print("number of non-nas:")
print(sum(!is.na(gram)))
gram[is.na(gram)]=0
print('nas have been cleaned. Writing file...')
write.table(gram,file="/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_eur_rare.txt",quote=F,sep="\t")
#write.table(gram,file="/hpc/hers_en/fsimoes/logs/objects/jaccard_gram_R_eur_common",quote=F,sep="\t")
print('END')
