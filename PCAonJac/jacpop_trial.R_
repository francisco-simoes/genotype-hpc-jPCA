#### Try the jacpop library on the genotype data adapting Kevin's code.

# Adapt following and execute using this specific R installation: /hpc/hers_en/shared/wxs/miniconda3/bin/R

# input data files
gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb" # our in-house format for genetic data, based on sqlite db
varSet=read.table("/hpc/hers_en/shared/wxs/mine_wxs_180919/varSets/moderate.exQCpass.txt.gz") # A table listing all protein altering variants detected in each gene. Each gene is one row, you can split this file to generate separate target files and then use a job array to have the cluster distribute analyses of different genes to different nodes before aggregating and doing PCA

#>>> Mine
install.packages('jacpop')
library(jacpop)
#<<< End

# gdb/file connections
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
varSet=gzcon(file(varSet,open="rb"))

# iterate through each gene in input varSet file
while (TRUE)
{
  # read the variants gene i
  i=readLines(varSet,n=1)
  if (length(i)==0){break}
  i=unlist(strsplit(i,split="\\|"))
  message(sprintf("Analysing %s",i[1]))
  unit=i[1]
  # extract the database ids for variants in target gene
  VAR_id=unlist(strsplit(i[2],split=","))
  # Load the sample genotypes for target variants
  GT=RVAT::loadGT(gdb, VAR_id)
  # Kick out everything except the rare variants
  GT$flipToMinor()
  GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0)
  # Calculate Jaccard similarity within this gene
# J=FranciscosFavoredJaccardDistanceFunction(GT$GT) #GT$GT is the matrix you are looking for, individual variant equivalent to what you have used until now
  res<-generate_pw_jaccard(geno=GT$GT, pop.label=???) #GT$GT is the matrix you are looking for, individual variant equivalent to what you have used until now
}

