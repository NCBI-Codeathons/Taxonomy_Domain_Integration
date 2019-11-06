# Build Sqlite DB, and overhead data for parallelizing FindSynteny
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

# no longer valid arguments
# Argument 1 == FASTA file / SeqSet
# Argument 2 == Sqlite file to generate / SqlFile
# Argument 3 == Generate RData file / RDataInitial

Arguments <- commandArgs(trailingOnly = TRUE)

suppressMessages(library(DECIPHER))

FNAs <- readDNAStringSet(filepath = Arguments[1L])
FNANames <- names(FNAs)

###### -- construct large sqlite database -------------------------------------

DBPATH <- paste(Arguments[2L],
                "/",
                "DBPATH.sqlite",
                sep = "")

pBar <- txtProgressBar(style = 1L)

for (m1 in seq_along(FNAs)) {
  Seqs2DB(seqs = FNAs[m1],
          type = "XStringSet",
          dbFile = DBPATH,
          identifier = as.character(m1),
          verbose = FALSE)
  setTxtProgressBar(pb = pBar,
                    value = m1 / length(FNAs))
}

cat("\n")

JobMap <- matrix(data = list(),
                 nrow = length(FNAs),
                 ncol = length(FNAs))
JobDim <- dim(JobMap)

for (m1 in seq_len(length(FNAs) - 1L)) {
  for (m2 in (m1 + 1L):length(FNAs)) {
    JobMap[[m1, m2]] <- c(m1, m2)
  }
}

JobMap <- do.call(rbind,
                  JobMap[upper.tri(JobMap)])

save(JobMap,
     FNANames,
     JobDim,
     file = paste(Arguments[2L],
                  "/",
                  "Initial.RData",
                  sep = ""))

