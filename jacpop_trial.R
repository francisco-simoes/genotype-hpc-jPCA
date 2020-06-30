#### Try the jacpop library on the genotype data adapting Kevin's code.

# Adapt following and execute using this specific R installation: /hpc/hers_en/shared/wxs/miniconda3/bin/Rscript

# input data files
gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb" # our in-house format for genetic data, based on sqlite db
#varSet=read.table("/hpc/hers_en/shared/wxs/mine_wxs_180919/varSets/moderate.exQCpass.txt.gz") # A table listing all protein altering variants detected in each gene. Each gene is one row, you can split this file to generate separate target files and then use a job array to have the cluster distribute analyses of different genes to different nodes before aggregating and doing PCA
varSet <- "/hpc/hers_en/shared/wxs/mine_wxs_180919/varSets/moderate.exQCpass.txt.gz" # Paul: table will be opened line-for-line further on
#>>> Mine
library(jacpop)
#<<< End

# gdb/file connections
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
varSet=gzcon(file(varSet,open="rb"))

#
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA") # Paul: load phenotype info 
# iterate through each gene in input varSet file
count = 1
increment = 10000
#while (TRUE)
while (count < increment*3) # run only for the first 3 batches.
{
#  # read the variants gene i
#  i=readLines(varSet,n=1)
#  if (length(i)==0){break}
#  i=unlist(strsplit(i,split="\\|"))
#  message(sprintf("Analysing %s",i[1]))
#  unit=i[1]
#  # extract the database ids for variants in target gene
  VAR_id=count:(count+increment) #This takes batches at a time.
  count = count+increment+1
#  VAR_id=unlist(strsplit(i[1000],split=","))
  # Load the sample genotypes for target variants
  GT=rvat::loadGT(gdb, VAR_id, SM=SM) # Paul: Changed RVAT to rvat
  keep=(!is.na(SM[,"pheno"])) & (SM[,"pheno"] %in% c(0,1))  
  GT$smFilter(keep==TRUE & GT$genoSM>0) # Paul: keep samples that are present in the 'SM' table (that pass QC)
  # Kick out everything except the rare variants
  GT$flipToMinor()
  #GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0) #genoVar>0 just makes sure that at least one of the rare variants is not an NA.
  GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7)
  # Get rid of NAs:
  GT$missingToRef() #NAs turn to zeros.
  # Calculate Jaccard similarity within this gene
  # J=FranciscosFavoredJaccardDistanceFunction(GT$GT) #GT$GT is the matrix you are looking for, individual variant equivalent to what you have used until now
  #>>> Mine
  #Make plots from jacpop function.
  png(file = sprintf("jacpop_count_%s_through_%s.png", count-increment-1, count), bg = "white")
  res<-generate_pw_jaccard(geno=GT$GT, pop.label=GT$SM$Site) #GT$GT is the matrix you are looking for, individual variant equivalent to what you have used until now
  dev.off() 
  # Save results in files.
  Jac = res[["Jac"]]
  pcs = res[["pcs"]]
  write.csv(Jac, sprintf("/hpc/hers_en/fsimoes/logs/objects/jacpop_trial_Jac_count_%s_through_%s.csv", count-increment-1, count))
  write.csv(pcs, sprintf("/hpc/hers_en/fsimoes/logs/objects/jacpop_trial_pcs_count_%s_through_%s.csv", count-increment-1, count))
  write.csv(GT$GT, sprintf("/hpc/hers_en/fsimoes/logs/objects/jacpop_trial_GT_count_%s_through_%s.csv", count-increment-1, count))
  #<<< End
}

