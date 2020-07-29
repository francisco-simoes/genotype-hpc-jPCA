library(jacpop)
# Note the VAR_id must be loaded from this file (these have been "LD pruned" as per Dmitry et al)
var=scan("/hpc/hers_en/kkenna/rvat_tutorial/variants.txt")
gdb="/hpc/hers_en/kkenna/rvat_tutorial/phase3_shapeit2_mvncall_integrated_v5a.20130502.gdb"
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
# Note this time the sample data comes from table "EUR" not "postPCA"
SM <- RSQLite::dbGetQuery(gdb, "select * from EUR")
print('before loadGT')
GT=rvat::loadGT(gdb, VAR_id=var, SM=SM)
print('before flipToMinor')
GT$flipToMinor()
GT$smFilter(!is.na(GT$SM$IID) & GT$SM$pheno %in% c(0,1))
# remove common variants (af>0.01) and singletons (af=1/(503*2)=0.0009940358)
GT$varFilter(GT$af<=0.01 & GT$af>0.0009940358)

png(file = sprintf("jacpop_count_%s_through_%s.png", count-increment-1, count), bg = "white")
print(dim(GT$GT))
res<-generate_pw_jaccard(geno=GT$GT, pop.label=GT$SM$Site) #GT$GT is the matrix you are looking for, individual variant equivalent to what you have used until now
dev.off() 
