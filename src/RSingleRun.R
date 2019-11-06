# Generate distance matrix for genome set
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, arguments, data ------------------------------------------

library(DECIPHER)

Arguments <- commandArgs(trailingOnly = TRUE)
suppressMessages(library(DECIPHER))
FNAs <- readDNAStringSet(filepath = Arguments[1L])

###### -- Generate distance matrix for sequences ------------------------------

FNANames <- names(FNAs)

DBPATH <- tempfile()

pBar <- txtProgressBar(style = 3L)
for (m1 in seq_along(FNAs)) {
  Seqs2DB(seqs = FNAs[m1],
          dbFile = DBPATH,
          type = "XStringSet",
          identifier = as.character(m1),
          verbose = FALSE)
  setTxtProgressBar(pb = pBar,
                    value = m1 / length(FNAs))
}

cat("/n")

# dropScore = 0 .. will attempt to extend blocks with alignment
Syn <- FindSynteny(dbFile = DBPATH,
                   verbose = TRUE,
                   dropScore = 0)

unlink(DBPATH)

Dists <- matrix(data = 0,
                nrow = nrow(Syn),
                ncol = ncol(Syn))

dimnames(Dists) <- list(dimnames(Syn)[[1]],
                        dimnames(Syn)[[2]])

for (m1 in seq_len(nrow(Syn) - 1L)) {
  for (m2 in (m1 + 1L):nrow(Syn)) {
    Dists[m1, m2] <- Dists[m2, m1] <- 1 - (2 * sum(Syn[[m1, m2]][, "width"])) / sum(Syn[[m1, m1]] + Syn[[m2, m2]])
  }
}

###### -- Save out matrix and names

NamesOut <- paste(seq(length(FNANames)),
                  FNANames,
                  sep = "_")

write.table(Dists,
            file = Arguments[2L],
            append = FALSE,
            quote = FALSE)

writeLines(NamesOut,
           Arguments[3L])

