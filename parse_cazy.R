# Load
df <- read.table(commandArgs(TRUE)[1], header = TRUE)
colnames(df) <- c(colnames(df)[2:6],"Tools")
df.sub <- df[df$Tools > 1,]

# Consensus
doms <- apply(df.sub, 1, function(x) gsub("\\(.*\\)","",unlist(strsplit(as.character(unlist(x[c(2,3,4)])), "\\+"))))
tabs <- lapply(as.list(doms), function(x) as.data.frame(table(x)))
cons <- lapply(tabs, function(x) as.character(x[order(x$Freq, decreasing = TRUE),][1,1]))
maxf <- lapply(tabs, function(x) max(x$Freq))

df.sub$Consensus <- unlist(cons)
df.sub$Cons.size <- unlist(maxf)

# Fix no consensus
no.cons <- df.sub[df.sub$Cons.size == 1, ]

# Fix sub family mismatches
doms2 <- apply(no.cons, 1,  function(x) gsub("_.*","",gsub("\\(.*\\)","",unlist(strsplit(as.character(unlist(x[c(2,3,4)])), "\\+")))))
tabs2 <- lapply(as.list(doms2), function(x) as.data.frame(table(x)))
cons2 <- lapply(tabs2, function(x) as.character(x[order(x$Freq, decreasing = TRUE),][1,1]))
maxf2 <- lapply(tabs2, function(x) max(x$Freq))

no.cons$Consensus <- unlist(cons2)
no.cons$Cons.size <- unlist(maxf2)

# Final
final <- rbind(df.sub[df.sub$Cons.size > 1, ],
               no.cons[no.cons$Cons.size > 1, ])

print(final[, c(1,7)], row.names = FALSE)

