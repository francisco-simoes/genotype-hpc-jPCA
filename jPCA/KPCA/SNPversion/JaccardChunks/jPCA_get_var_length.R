gdb="/hpc/hers_en/shared/wxs/mine_wxs_180919/gdb/mine_wxs_180919.gdb"   
gdb=RSQLite::dbConnect(RSQLite::dbDriver("SQLite"),gdb)
SM <- RSQLite::dbGetQuery(gdb, "select * from postPCA")
var=scan("VAR_id.txt") #Create txt with `echo "select VAR_id from exQCpass" | sqlite3 $gdb`
print('Total var number:')
print(length(var))
memlimit=10000 #Number of variants to use in each batch.
if (length(var)>memlimit){var=split(var, cut(seq_along(var), ceiling(length(var)/memlimit), labels = FALSE))}else{var=list(var)} #Divide `var` in chunks.
print('Number of chunks:')
print(length(var))
