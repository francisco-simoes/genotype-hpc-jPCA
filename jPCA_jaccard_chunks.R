gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb | head`
memlimit=10000 #Number of variants to use in each batch.
if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)}m11=matrix(0,nrow=nrow(SM),ncol=ncol(SM))
m01=matrix(0,nrow=nrow(SM),ncol=ncol(SM)) 
#m11...
#m22...
for (i in 1:length(var))
{
  # Load the sample genotypes for target variants
  GT=rvat::loadGT(gdb, var[i], SM=SM)  # Kick out everything except the rare variants
  GT$flipToMinor()
  # kick out everything except rare high call rate variants
  GT$varFilter(GT$af<=0.001 & GT$af>0 & GT$genoVar>0.7)
  # kick out everything except common high call rate variants
  #GT$varFilter(GT$af>=0.01 & GT$genoVar>0.7)
  # Get rid of NAs:
  GT$missingToRef() #NAs turn to zeros.  for (i in 1:now(SM))
  {
    for(j in 1:nrow(SM))
    {
      m11i=sum(GT$GT[i,] == 1 & GT$GT[j,] == 1)
    	#...
    }
  }}
dist=(m11 / (m11 + m10 + m01))
write.table(dist,file="xxxxx",quote=F,sep="\t")
