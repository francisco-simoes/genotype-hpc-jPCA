gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")

Equal_positive_count=matrix(0,nrow=nrow(SM),ncol=nrow(SM)) #Replaces M11,M22.

equal_positive_count = load("/hpc/hers_en/fsimoes/jPCA/JaccardChunks/mijs/eq_pos_count_1.rda")
print(equal_positive_count)
print(typeof(equal_positive_count))
